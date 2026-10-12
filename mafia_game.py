import asyncio
import logging
import asyncio
import random
from typing import Optional

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

# Set this from bot.py after init_db() has created the asyncpg pool.
DB_POOL = None

ENTRY_FEE = 10000
NIGHT_SECONDS = 20
VOTE_SECONDS = 30
MIN_PLAYERS = 4
MAX_PLAYERS = 15

MAFIA_GAMES = {}
async def mafia_lobby_timeout(context, chat_id):
    await asyncio.sleep(60)

    game = MAFIA_GAMES.get(chat_id)

    if not game or game.get("closed"):
        return

    if game.get("phase") != "lobby":
        return

    if len(game.get("players", {})) < 4:
        game["closed"] = True

        await context.bot.send_message(
            chat_id=chat_id,
            text=(
                "⏰ Mafia Game အလိုအလျောက် ပိတ်လိုက်ပါပြီ။\n\n"
                "❌ ၁ မိနစ်အတွင်း ကစားသမား ၄ ယောက် "
                "မပြည့်လို့ ပွဲမစနိုင်ပါဘူး။\n"
                "🎮 နောက်တစ်ကြိမ် /mafia နဲ့ ပြန်စနိုင်ပါတယ်။"
            ),
        )

def set_db_pool(pool):
    """Pass bot.py's existing asyncpg pool into this module."""
    global DB_POOL
    DB_POOL = pool


def player_name(user):
    return user.full_name or user.username or str(user.id)


def mafia_status(game):
    alive = [p for p in game["players"].values() if p["alive"]]
    mafia = sum(p["role"] == "Mafia" for p in alive)
    town = len(alive) - mafia

    if mafia == 0:
        return "town"
    if mafia >= town:
        return "mafia"
    return None


def lobby_keyboard(chat_id):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎭 Join Game", callback_data=f"mafia:join:{chat_id}")],
        [InlineKeyboardButton("▶️ Start Game", callback_data=f"mafia:start:{chat_id}")],
    ])


def mafia_keyboard(chat_id, players, action):
    rows = []
    for uid, player in players.items():
        if player.get("alive", True):
            rows.append([
                InlineKeyboardButton(
                    player["name"][:60],
                    callback_data=f"mafia:{action}:{chat_id}:{uid}",
                )
            ])
    return InlineKeyboardMarkup(rows) if rows else InlineKeyboardMarkup([])


async def _deduct_entry_fee(user_id):
    """Atomic deduction; returns (success, reason, new_balance)."""
    if DB_POOL is None:
        return False, "database", None

    async with DB_POOL.acquire() as conn:
        row = await conn.fetchrow(
            """
            UPDATE users
            SET coins = coins - $1, updated_at = NOW()
            WHERE telegram_id = $2 AND coins >= $1
            RETURNING coins
            """,
            ENTRY_FEE,
            user_id,
        )
    if row is None:
        exists = await DB_POOL.fetchval(
            "SELECT 1 FROM users WHERE telegram_id = $1",
            user_id,
        )
        return (False, "balance" if exists else "unregistered", None)
    return True, "ok", row["coins"]


async def _refund_players(game):
    """Refund every fee paid into this game exactly once."""
    if game.get("refunded") or game.get("paid_out"):
        return
    if DB_POOL is None:
        raise RuntimeError("Database pool is not configured")

    async with DB_POOL.acquire() as conn:
        async with conn.transaction():
            for uid, player in game["players"].items():
                if player.get("fee_paid"):
                    await conn.execute(
                        """
                        UPDATE users
                        SET coins = coins + $1, updated_at = NOW()
                        WHERE telegram_id = $2
                        """,
                        ENTRY_FEE,
                        uid,
                    )
                    player["fee_paid"] = False
    game["refunded"] = True


async def _payout_winners(game, winner):
    """Split the full entry-fee pot evenly among the winning faction."""
    if game.get("paid_out"):
        return {}
    if DB_POOL is None:
        raise RuntimeError("Database pool is not configured")

    winning_players = [
        (uid, p) for uid, p in game["players"].items()
        if (p["role"] == "Mafia" if winner == "mafia" else p["role"] != "Mafia")
    ]
    if not winning_players:
        return {}

    pot = sum(ENTRY_FEE for p in game["players"].values() if p.get("fee_paid"))
    if pot <= 0:
        game["paid_out"] = True
        return {}

    winning_players.sort(key=lambda item: item[0])
    share, remainder = divmod(pot, len(winning_players))
    payouts = {}

    async with DB_POOL.acquire() as conn:
        async with conn.transaction():
            for index, (uid, player) in enumerate(winning_players):
                amount = share + (1 if index < remainder else 0)
                if amount:
                    row = await conn.fetchrow(
                        """
                        UPDATE users
                        SET coins = coins + $1, updated_at = NOW()
                        WHERE telegram_id = $2
                        RETURNING coins
                        """,
                        amount,
                        uid,
                    )
                    if row is None:
                        raise RuntimeError(f"User {uid} missing during Mafia payout")
                    payouts[uid] = amount

    game["paid_out"] = True
    return payouts


async def mafia_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    chat = update.effective_chat
    user = update.effective_user

    if not message or not chat or not user:
        return
    if chat.type not in ("group", "supergroup"):
        await message.reply_text("⚠️ Mafia Game ကို Group ထဲမှာပဲ ဖွင့်နိုင်ပါတယ်။")
        return
    if DB_POOL is None:
        await message.reply_text("⚠️ Database မချိတ်ဆက်ရသေးပါ။ Bot ကို ပြန်စတင်ပါ။")
        return

    old_game = MAFIA_GAMES.get(chat.id)
    if old_game and not old_game.get("closed"):
        await message.reply_text("🎭 ဒီ Group မှာ Mafia Game ရှိနေပါပြီ။")
        return

    MAFIA_GAMES[chat.id] = {
        "host": user.id,
        "host_name": player_name(user),
        "players": {},
        "phase": "lobby",
        "votes": {},
        "night_actions": {},
        "closed": False,
        "day": 0,
        "pot": 0,
        "refunded": False,
        "paid_out": False,
        "phase_token": 0,
        "lock": asyncio.Lock(),
    }

    await message.reply_text(
        "🎭 QUICK MAFIA\n"
        "━━━━━━━━━━━━━━\n"
        f"🪙 ဝင်ကြေး — တစ်ယောက် {ENTRY_FEE:,} Coins\n"
        f"👥 အနည်းဆုံး {MIN_PLAYERS} ယောက် လိုအပ်ပါတယ်။\n"
        "⏱️ ညဘက် ၂၀ စက္ကန့် | Vote ၃၀ စက္ကန့်\n\n"
        "🎭 Role များ — Mafia, Doctor, Detective, Villager\n"
        "🔐 Role ရရန် Bot ကို Private မှာ /start လုပ်ထားပါ။\n"
        "▶️ Host က Start နှိပ်ပြီး ဂိမ်းစနိုင်ပါတယ်။",
        reply_markup=lobby_keyboard(chat.id),
    )


async def mafia_stop_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    chat = update.effective_chat
    user = update.effective_user
    if not message or not chat or not user:
        return
    game = MAFIA_GAMES.get(chat.id)
    if not game or game.get("closed"):
        await message.reply_text("❌ ဒီ Group မှာ လက်ရှိ Mafia Game မရှိပါ။")
        return
    if user.id != game["host"]:
        await message.reply_text("❌ Game ဖွင့်ထားသူပဲ /mafiastop လုပ်နိုင်ပါတယ်။")
        return

    try:
        await _refund_players(game)
    except Exception:
        logger.exception("Mafia refund failed")
        await message.reply_text("⚠️ Coin ပြန်အမ်းရာမှာ Error ဖြစ်နေပါတယ်။ Admin ကို ဆက်သွယ်ပါ။")
        return

    game["closed"] = True
    game["phase"] = "finished"
    game["phase_token"] += 1
    await message.reply_text(
        f"🛑 Mafia Game ကို ဖျက်သိမ်းလိုက်ပါပြီ။\n"
        f"🪙 ဝင်ကြေး {ENTRY_FEE:,} Coins ကို ကစားသမားများထံ ပြန်အမ်းပြီးပါပြီ။"
    )
    asyncio.create_task(
        mafia_lobby_timeout(context, chat.id)
    )

async def mafia_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if not query or not query.data:
        return

    parts = query.data.split(":")
    if len(parts) < 3 or parts[0] != "mafia":
        await query.answer()
        return

    action = parts[1]
    try:
        chat_id = int(parts[2])
    except ValueError:
        await query.answer("❌ Invalid game.", show_alert=True)
        return

    game = MAFIA_GAMES.get(chat_id)
    if not game or game.get("closed"):
        await query.answer("❌ ဒီဂိမ်း ပြီးဆုံးသွားပါပြီ။", show_alert=True)
        return

    user = query.from_user
    user_id = user.id

    if action == "join":
        # Telegram callback ကို ချက်ချင်းဖြေကြားပါ။
        await query.answer()

        # ကစားသမားက Join လုပ်ပြီးသားလား စစ်ပါ။
        if user_id in game["players"]:
            await query.message.reply_text(
                "✅ သင် Game ထဲဝင်ပြီးသားပါ။"
            )
            return

        # ကစားသမားအများဆုံးအရေအတွက် စစ်ပါ။
        if len(game["players"]) >= MAX_PLAYERS:
            await query.message.reply_text(
                f"❌ Player အများဆုံး {MAX_PLAYERS} ယောက်သာ ဝင်နိုင်ပါတယ်။"
            )
            return

        # ဝင်ကြေးဖြတ်ပါ။
        ok, reason, balance = await _deduct_entry_fee(user_id)

        if not ok:
            messages = {
                "database": "⚠️ Database ချိတ်ဆက်မှု အမှားရှိနေပါတယ်။",
                "balance": (
                    f"❌ Coin မလုံလောက်ပါ။ "
                    f"ဝင်ကြေး {ENTRY_FEE} Coins လိုအပ်ပါတယ်။"
                ),
                "unregistered": (
                    "❌ Bot မှာ /start နှိပ်ပြီး Register လုပ်ပါ။"
                ),
            }

            await query.message.reply_text(
                messages.get(reason, "❌ Join မအောင်မြင်ပါ။")
            )
            return

        # ကစားသမားကို Game ထဲထည့်ပါ။
        game["players"][user_id] = {
            "user": user,
            "name": player_name(user),
            "role": None,
            "alive": True,
            "fee_paid": True,
        }

        # Pot ထဲ ဝင်ကြေးပေါင်းထည့်ပါ။
        game["pot"] += ENTRY_FEE

        # ကစားသမားစာရင်း ပြင်ဆင်ပါ။
        names = "\n".join(
            f"• {p['name']}"
            for p in game["players"].values()
        )

        # Lobby message ကို Update လုပ်ပါ။
        try:
            await query.edit_message_text(
                "🎭 QUICK MAFIA\n"
                "━━━━━━━━━━━━━━\n"
                f"👥 Player: {len(game['players'])} ယောက်\n"
                f"🪙 Pot: {game['pot']:,} Coins\n\n"
                f"{names}\n\n"
                "Join Game ခလုတ်ကို နှိပ်ပါ။",
                reply_markup=lobby_keyboard(chat_id),
            )
        except Exception as exc:
            logger.warning(
                "Mafia lobby update failed: %s", exc
            )

        return

    if action == "start":
        async with game["lock"]:
            if user_id != game["host"]:
                await query.answer("❌ Game ဖွင့်ထားသူပဲ Start လုပ်နိုင်ပါတယ်။", show_alert=True)
                return
            if game["phase"] != "lobby":
                await query.answer("⏳ Game စတင်နေပါပြီ။", show_alert=True)
                return
            if len(game["players"]) < MIN_PLAYERS:
                await query.answer(f"အနည်းဆုံး လူ {MIN_PLAYERS} ယောက် လိုအပ်ပါတယ်။", show_alert=True)
                return

            game["phase"] = "starting"
            ids = list(game["players"])
            random.shuffle(ids)
            mafia_count = max(1, len(ids) // 4)
            roles = (
                ["Mafia"] * mafia_count
                + ["Doctor", "Detective"]
                + ["Villager"] * (len(ids) - mafia_count - 2)
            )
            random.shuffle(roles)
            for uid, role in zip(ids, roles):
                game["players"][uid]["role"] = role

            descriptions = {
                "Mafia": "🔪 သင်သည် Mafia ဖြစ်ပါတယ်။ ညပိုင်းတွင် ပစ်မှတ်ရွေးပါ။",
                "Doctor": "💊 သင်သည် Doctor ဖြစ်ပါတယ်။ ညပိုင်းတွင် ကယ်တင်မည့်သူကို ရွေးပါ။",
                "Detective": "🕵️ သင်သည် Detective ဖြစ်ပါတယ်။ ညပိုင်းတွင် စစ်ဆေးမည့်သူကို ရွေးပါ။",
                "Villager": "👨‍🌾 သင်သည် Villager ဖြစ်ပါတယ်။ နေ့ပိုင်းတွင် မဲပေးပါ။",
            }
            try:
                for uid in ids:
                    await context.bot.send_message(
                        chat_id=uid,
                        text="🎭 QUICK MAFIA — YOUR ROLE\n\n" + descriptions[game["players"][uid]["role"]],
                    )
            except Exception:
                logger.exception("Could not send Mafia role DM")
                try:
                    await _refund_players(game)
                except Exception:
                    logger.exception("Mafia refund after DM failure failed")
                game["closed"] = True
                game["phase"] = "finished"
                await query.answer("⚠️ တစ်ယောက်ယောက်က Bot ကို Private မှာ /start မလုပ်ထားပါ။", show_alert=True)
                await query.message.reply_text(
                    "⚠️ Role ပို့မရပါ။ Game ဖျက်သိမ်းပြီး ဝင်ကြေးပြန်အမ်းရန် ကြိုးစားပြီးပါပြီ။ "
                    "အားလုံး Bot ကို Private မှာ /start လုပ်ပြီး Game အသစ်ဖွင့်ပါ။"
                )
                return

            await query.answer("🎮 Game စတင်ပါပြီ။")
            try:
                await query.edit_message_reply_markup(reply_markup=None)
            except Exception:
                pass

            game["day"] = 1
            game["phase"] = "night"
            game["night_actions"] = {}
            game["phase_token"] += 1
            token = game["phase_token"]

        await context.bot.send_message(
            chat_id=chat_id,
            text=f"🌙 ညပိုင်း စတင်ပါပြီ။ ({NIGHT_SECONDS} စက္ကန့်)\n"
                 "Mafia, Doctor နဲ့ Detective တို့ Private Chat မှာ ရွေးချယ်ပါ။",
        )
        await send_night_actions(context, chat_id, game)
        asyncio.create_task(_night_timeout(context, chat_id, game, token))
        return

    if action == "night":
        if len(parts) != 4:
            await query.answer()
            return
        try:
            target_id = int(parts[3])
        except ValueError:
            await query.answer("❌ Invalid target.", show_alert=True)
            return

        if game["phase"] != "night":
            await query.answer("⏳ ညပိုင်း မဟုတ်တော့ပါ။", show_alert=True)
            return
        actor = game["players"].get(user_id)
        target = game["players"].get(target_id)
        if not actor or not actor["alive"] or not target or not target["alive"]:
            await query.answer("❌ ဒီရွေးချယ်မှု မရနိုင်ပါ။", show_alert=True)
            return
        if actor["role"] not in ("Mafia", "Doctor", "Detective"):
            await query.answer("❌ သင့် Role မှာ Night Action မရှိပါ။", show_alert=True)
            return
        if user_id in game["night_actions"]:
            await query.answer("✅ ဒီညအတွက် ရွေးချယ်ပြီးပါပြီ။", show_alert=True)
            return
        if actor["role"] == "Mafia" and target["role"] == "Mafia":
            await query.answer("❌ ကိုယ့်အဖွဲ့ဝင်ကို ရွေးလို့မရပါ။", show_alert=True)
            return

        game["night_actions"][user_id] = {"role": actor["role"], "target": target_id}
        if actor["role"] == "Detective":
            try:
                await context.bot.send_message(
                    chat_id=user_id,
                    text=f"🕵️ စစ်ဆေးချက်\n\n👤 {target['name']}\n🎭 Role: {target['role']}",
                )
            except Exception:
                logger.exception("Could not send Detective result")
        await query.answer("✅ ရွေးချယ်မှု မှတ်တမ်းတင်ပြီးပါပြီ။")
        try:
            await query.edit_message_text("✅ ဒီညအတွက် ရွေးချယ်မှု မှတ်တမ်းတင်ပြီးပါပြီ။")
        except Exception:
            pass
        await check_night_complete(context, chat_id, game)
        return

    if action == "vote":
        if len(parts) != 4:
            await query.answer()
            return
        try:
            target_id = int(parts[3])
        except ValueError:
            await query.answer("❌ Invalid target.", show_alert=True)
            return
        if game["phase"] != "day":
            await query.answer("⏳ မဲပေးချိန် မဟုတ်ပါ။", show_alert=True)
            return
        actor = game["players"].get(user_id)
        target = game["players"].get(target_id)
        if not actor or not actor["alive"] or not target or not target["alive"]:
            await query.answer("❌ မဲပေးလို့မရပါ။", show_alert=True)
            return
        if user_id == target_id:
            await query.answer("❌ ကိုယ့်ကိုယ်ကို မဲပေးလို့မရပါ။", show_alert=True)
            return
        if user_id in game["votes"]:
            await query.answer("✅ မဲပေးပြီးပါပြီ။", show_alert=True)
            return

        game["votes"][user_id] = target_id
        await query.answer("🗳️ မဲပေးပြီးပါပြီ။")
        alive_count = sum(p["alive"] for p in game["players"].values())
        if len(game["votes"]) >= alive_count:
            await resolve_day(context, chat_id, game)
        return

    await query.answer()


async def send_night_actions(context, chat_id, game):
    players = game["players"]
    for uid, player in players.items():
        if not player["alive"]:
            continue
        role = player["role"]
        if role not in ("Mafia", "Doctor", "Detective"):
            continue

        targets = {
            tid: target for tid, target in players.items()
            if target["alive"]
            and tid != uid
            and not (role == "Mafia" and target["role"] == "Mafia")
        }
        if not targets:
            game["night_actions"][uid] = {"role": role, "target": None}
            continue

        prompts = {
            "Mafia": "🔪 ဘယ်သူ့ကို ဖယ်ရှားမလဲ?",
            "Doctor": "💊 ဘယ်သူ့ကို ကယ်တင်မလဲ?",
            "Detective": "🕵️ ဘယ်သူ့ကို စစ်ဆေးမလဲ?",
        }
        try:
            await context.bot.send_message(
                chat_id=uid,
                text=prompts[role] + f"\n⏱️ {NIGHT_SECONDS} စက္ကန့်အတွင်း ရွေးပါ။",
                reply_markup=mafia_keyboard(chat_id, targets, "night"),
            )
        except Exception:
            logger.warning("Could not send night action to %s", uid)

    await check_night_complete(context, chat_id, game)


async def _night_timeout(context, chat_id, game, token):
    await asyncio.sleep(NIGHT_SECONDS)
    if game.get("closed") or game["phase"] != "night" or game["phase_token"] != token:
        return
    await resolve_night(context, chat_id, game, timed_out=True)


async def check_night_complete(context, chat_id, game):
    if game["phase"] != "night":
        return
    required = [
        uid for uid, p in game["players"].items()
        if p["alive"] and p["role"] in ("Mafia", "Doctor", "Detective")
    ]
    if all(uid in game["night_actions"] for uid in required):
        await resolve_night(context, chat_id, game, timed_out=False)


async def resolve_night(context, chat_id, game, timed_out=False):
    if game.get("closed") or game["phase"] != "night":
        return

    # Change phase first so a timeout and a final button click cannot resolve twice.
    game["phase"] = "resolving_night"
    game["phase_token"] += 1
    actions = list(game["night_actions"].values())
    mafia_votes = [
        a["target"] for a in actions
        if a["role"] == "Mafia" and a["target"] is not None
    ]
    doctor_targets = [
        a["target"] for a in actions
        if a["role"] == "Doctor" and a["target"] is not None
    ]

    killed = None
    if mafia_votes:
        counts = {target: mafia_votes.count(target) for target in set(mafia_votes)}
        highest = max(counts.values())
        choices = [target for target, count in counts.items() if count == highest]
        killed = random.choice(choices)

    if killed is not None and killed in doctor_targets:
        killed = None
    if killed is not None and killed in game["players"]:
        game["players"][killed]["alive"] = False
        result = f"🌅 မနက်ခင်း ရောက်ပါပြီ!\n\n💀 {game['players'][killed]['name']} သည် ညပိုင်းတွင် သေဆုံးသွားပါတယ်။"
    else:
        result = "🌅 မနက်ခင်း ရောက်ပါပြီ!\n\n✨ ဒီညမှာ ဘယ်သူမှ မသေဆုံးပါ။"

    winner = mafia_status(game)
    if winner:
        await end_mafia_game(context, chat_id, game, winner)
        return

    game["phase"] = "day"
    game["votes"] = {}
    game["phase_token"] += 1
    token = game["phase_token"]
    await context.bot.send_message(
        chat_id=chat_id,
        text=result + f"\n\n🗳️ မဲပေးချိန် ({VOTE_SECONDS} စက္ကန့်) စတင်ပါပြီ။",
        reply_markup=mafia_keyboard(chat_id, game["players"], "vote"),
    )
    asyncio.create_task(_day_timeout(context, chat_id, game, token))


async def _day_timeout(context, chat_id, game, token):
    await asyncio.sleep(VOTE_SECONDS)
    if game.get("closed") or game["phase"] != "day" or game["phase_token"] != token:
        return
    await resolve_day(context, chat_id, game, timed_out=True)


async def resolve_day(context, chat_id, game, timed_out=False):
    if game.get("closed") or game["phase"] != "day":
        return
    game["phase"] = "resolving_day"
    game["phase_token"] += 1

    counts = {}
    for target in game["votes"].values():
        counts[target] = counts.get(target, 0) + 1

    if not counts:
        result = "🗳️ မဲပေးချိန်ကုန်ပါပြီ။ မဲမရှိသဖြင့် ဒီနေ့ ဘယ်သူမှ မထွက်ရပါ။"
    else:
        highest = max(counts.values())
        choices = [uid for uid, count in counts.items() if count == highest]
        if len(choices) == 1:
            eliminated = choices[0]
            game["players"][eliminated]["alive"] = False
            result = (
                "🗳️ မဲပေးမှု ရလဒ်\n\n"
                f"⚖️ {game['players'][eliminated]['name']} ကို ဖယ်ရှားလိုက်ပါပြီ။\n"
                f"🎭 Role: {game['players'][eliminated]['role']}"
            )
        else:
            result = "🗳️ မဲပေးမှု သရေကျသွားပါတယ်။ ဒီနေ့ ဘယ်သူမှ မထွက်ရပါ။"

    winner = mafia_status(game)
    if winner:
        await end_mafia_game(context, chat_id, game, winner)
        return

    game["day"] += 1
    game["phase"] = "night"
    game["night_actions"] = {}
    game["phase_token"] += 1
    token = game["phase_token"]
    await context.bot.send_message(
        chat_id=chat_id,
        text=result + f"\n\n🌙 ညပိုင်း ပြန်စပါပြီ။ ({NIGHT_SECONDS} စက္ကန့်)",
    )
    await send_night_actions(context, chat_id, game)
    if game["phase"] == "night":
        asyncio.create_task(_night_timeout(context, chat_id, game, token))


async def end_mafia_game(context, chat_id, game, winner):
    if game.get("closed") or game["phase"] in ("settling", "finished"):
        return
    game["phase"] = "settling"
    try:
        payouts = await _payout_winners(game, winner)
    except Exception:
        logger.exception("Mafia payout failed")
        game["closed"] = True
        game["phase"] = "finished"
        await context.bot.send_message(
            chat_id=chat_id,
            text="⚠️ Game ပြီးဆုံးပါပြီ၊ ဒါပေမဲ့ Coin ဆုကြေးပေးရာမှာ Database Error ဖြစ်နေပါတယ်။ Admin ကို ဆက်သွယ်ပါ။",
        )
        return

    game["closed"] = True
    game["phase"] = "finished"
    title = "🔪 MAFIA အဖွဲ့ အနိုင်ရပါပြီ!" if winner == "mafia" else "🏆 ရွာသားအဖွဲ့ အနိုင်ရပါပြီ!"

    results = []
    for player in game["players"].values():
        status = "💚 အသက်ရှင်" if player["alive"] else "💀 သေဆုံး"
        results.append(f"{status} — {player['name']}: {player['role']}")

    payout_lines = []
    for uid, amount in payouts.items():
        payout_lines.append(f"• {game['players'][uid]['name']} — +{amount:,} Coins")

    payout_text = "\n".join(payout_lines) if payout_lines else "ဆုကြေးပေးချေမှု မရှိပါ။"
    await context.bot.send_message(
        chat_id=chat_id,
        text=(
            f"{title}\n\n"
            "🎭 ကစားသမားများ၏ Role\n\n"
            + "\n".join(results)
            + f"\n\n🪙 ဆုကြေး (Pot: {game['pot']:,} Coins)\n"
            + payout_text
            + "\n\n🔄 နောက်တစ်ပွဲကစားရန် /mafia ကိုနှိပ်ပါ။"
        ),
    )

