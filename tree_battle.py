"""Tree Cutting 1v1 battle for the existing python-telegram-bot project."""
import random
from pathlib import Path
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from game_cleanup import hide_command, reply_and_expire, photo_and_expire, schedule_delete

_pool = None
_games = {}
_ASSET_DIR = Path(__file__).resolve().parent / "assets" / "tree_battle"

def set_db_pool(pool):
    global _pool
    _pool = pool

async def _expire_waiting_battle(context, chat_id, message_id):
    import asyncio
    await asyncio.sleep(60)
    game = _games.get(chat_id)
    if game and game.get("state") == "waiting":
        _games.pop(chat_id, None)
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
        except Exception:
            pass


async def treebattle_command(update, context):
    msg = update.effective_message
    context.application.create_task(hide_command(context, msg))
    user = update.effective_user
    if not msg or not user or msg.chat.type == "private":
        if msg: await reply_and_expire(msg, context, "ဒီဂိမ်းကို Group ထဲမှာ ကစားပါ။")
        return
    if msg.chat_id in _games:
        await reply_and_expire(msg, context, 
            "ဒီ Group မှာ Battle တစ်ခု ကျန်နေပါတယ်။\n"
            "အရင်ပွဲကို ဖျက်/ပြန်စဖို့ ပွဲဖန်တီးသူက /treecancel ကို သုံးပါ။"
        )
        return
    try:
        bet = int(context.args[0]) if context.args else 10
    except ValueError:
        await reply_and_expire(msg, context, "အသုံးပြုပုံ: /treebattle [coin]\nဥပမာ: /treebattle 100")
        return
    if bet < 1 or bet > 100000:
        await reply_and_expire(msg, context, "Bet ကို 1 မှ 100000 Coins အတွင်း ထည့်ပါ။")
        return
    if not _pool:
        await reply_and_expire(msg, context, "ဂိမ်းဒေတာဘေ့စ် မချိတ်ဆက်ရသေးပါ။")
        return
    row = await _pool.fetchrow("SELECT coins FROM users WHERE telegram_id=$1", user.id)
    if not row:
        await reply_and_expire(msg, context, "အရင်ဆုံး Bot မှာ /start နဲ့ Register လုပ်ပါ။")
        return
    if row["coins"] < bet:
        await reply_and_expire(msg, context, f"Coin မလုံလောက်ပါ။ လက်ကျန် {row['coins']} Coins")
        return
    _games[msg.chat_id] = {"host": user.id, "host_name": user.full_name, "bet": bet,
                           "hp": {user.id: 100}, "names": {user.id: user.full_name}, "turn": user.id,
                           "state": "waiting"}
    kb = InlineKeyboardMarkup([[InlineKeyboardButton("🪓 Battle ဝင်မယ်", callback_data=f"tree:join:{msg.chat_id}")]])
    caption = f"🌲 TREE CUTTING 1Vs1 BATTLE 🌲\n\n🪓 စိန်ခေါ်သူ: {user.full_name}\n💰 လောင်းကြေး: {bet} Coins / တစ်ယောက်\n❤️ HP: 100 vs 100\n\nဒုတိယကစားသမားက ဝင်ရောက်ပါ။"
    with open(_ASSET_DIR / "battle_arena.png", "rb") as photo:
        battle_msg = await msg.reply_photo(photo=photo, caption=caption, reply_markup=kb)
        _games[msg.chat_id]["message_id"] = battle_msg.message_id
        # A waiting challenge expires after one minute; active battles remain visible.
        context.application.create_task(_expire_waiting_battle(context, msg.chat_id, battle_msg.message_id))

async def _delete_finished_battle(context, chat_id, message_id):
    import asyncio
    await asyncio.sleep(60)
    try:
        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception:
        pass


async def treebattle_callback(update, context):
    q = update.callback_query
    user = q.from_user
    parts = q.data.split(":")
    try: chat_id = int(parts[2])
    except (ValueError, IndexError):
        await q.answer("ဂိမ်းအချက်အလက် မမှန်ပါ။", show_alert=True); return
    game = _games.get(chat_id)
    if not game:
        await q.answer("ဒီဂိမ်း ပြီးဆုံးသွားပါပြီ။", show_alert=True); return
    if parts[1] == "join":
        if game["state"] != "waiting": await q.answer("Battle စတင်ပြီးပါပြီ။", show_alert=True); return
        if user.id == game["host"]: await q.answer("ကိုယ့်ကိုယ်ကို ပြိုင်ဘက်အဖြစ် ဝင်လို့မရပါ။", show_alert=True); return
        row = await _pool.fetchrow("SELECT coins FROM users WHERE telegram_id=$1", user.id)
        if not row: await q.answer("အရင်ဆုံး /start နဲ့ Register လုပ်ပါ။", show_alert=True); return
        if row["coins"] < game["bet"]: await q.answer("Coin မလုံလောက်ပါ။", show_alert=True); return
        async with _pool.acquire() as conn:
            async with conn.transaction():
                for uid in (game["host"], user.id):
                    res = await conn.execute("UPDATE users SET coins=coins-$1 WHERE telegram_id=$2 AND coins >= $1", game["bet"], uid)
                    if res != "UPDATE 1": raise ValueError("insufficient coins")
        game["hp"][user.id] = 100; game["names"][user.id] = user.full_name
        game["players"] = [game["host"], user.id]; game["turn"] = game["host"]; game["state"] = "playing"
        await q.answer("Battle စတင်ပါပြီ!")
        await q.edit_message_caption(caption=_status(game), reply_markup=_buttons(chat_id, game))
        return
    if parts[1] == "chop":
        if game["state"] != "playing": await q.answer("Battle မကစားနိုင်တော့ပါ။", show_alert=True); return
        if user.id not in game["players"]: await q.answer("ဒီ Battle ရဲ့ ကစားသမား မဟုတ်ပါ။", show_alert=True); return
        if game["turn"] != user.id: await q.answer("အခု သင့်အလှည့် မဟုတ်သေးပါ။", show_alert=True); return
        opponent = next(pid for pid in game["players"] if pid != user.id)
        damage = random.randint(15, 35)
        game["hp"][opponent] = max(0, game["hp"][opponent] - damage)
        if game["hp"][opponent] == 0:
            winner = user.id
            await _pool.execute("UPDATE users SET coins=coins+$1 WHERE telegram_id=$2", game["bet"] * 2, winner)
            game["state"] = "finished"
            await q.answer(f"🪓 {damage} damage! သင်နိုင်ပါပြီ!")
            with open(_ASSET_DIR / "victory.png", "rb") as photo:
                await q.edit_message_media(media=InputMediaPhoto(media=photo, caption=_status(game, winner=winner)), reply_markup=None)
            # Keep the final result visible for one minute, then remove it.
            context.application.create_task(_delete_finished_battle(context, chat_id, q.message.message_id))
            _games.pop(chat_id, None)
        else:
            game["turn"] = opponent
            await q.answer(f"🪓 {damage} damage!")
            await q.edit_message_caption(caption=_status(game), reply_markup=_buttons(chat_id, game))

def _status(g, winner=None):
    a, b = (g["players"] if "players" in g else [g["host"]])
    text = "🌲 TREE CUTTING BATTLE\n\n"
    for uid in (a, b):
        hp = g["hp"].get(uid, 100)
        text += f"🪓 {g['names'][uid]}\n❤️ {'🟩' * (hp // 10)}{'⬜' * ((100-hp)//10)} {hp}/100\n\n"
    text += f"💰 ဆုကြေး: {g['bet']*2} Coins\n"
    if winner: text += f"\n🏆 အနိုင်ရသူ: {g['names'][winner]}"
    elif g["state"] == "playing": text += f"\n🎯 အလှည့်: {g['names'][g['turn']]}"
    return text

def _buttons(chat_id, g):
    return InlineKeyboardMarkup([[InlineKeyboardButton("🪓 သစ်ပင်ခုတ်မယ်", callback_data=f"tree:chop:{chat_id}")]])


async def treebattle_cancel_command(update, context):
    """Cancel a stuck/waiting battle; refund stakes if a match had started."""
    msg = update.effective_message
    context.application.create_task(hide_command(context, msg))
    user = update.effective_user
    if not msg or not user or msg.chat.type == "private":
        if msg:
            await reply_and_expire(msg, context, "ဒီ Command ကို Group ထဲမှာ သုံးပါ။")
        return

    game = _games.get(msg.chat_id)
    if not game:
        await reply_and_expire(msg, context, "ဒီ Group မှာ ဖျက်စရာ Battle မရှိပါ။")
        return
    if user.id != game.get("host"):
        await reply_and_expire(msg, context, "Battle ကို စတင်ထားသူသာ /treecancel လုပ်နိုင်ပါတယ်။")
        return

    # Stakes are charged only after the second player joins.
    # If already playing, refund both players before clearing the game.
    if game.get("state") == "playing" and _pool:
        players = game.get("players", [])
        if players:
            async with _pool.acquire() as conn:
                async with conn.transaction():
                    for uid in players:
                        await conn.execute(
                            "UPDATE users SET coins=coins+$1 WHERE telegram_id=$2",
                            game["bet"], uid
                        )

    old_message_id = game.get("message_id")
    _games.pop(msg.chat_id, None)
    if old_message_id:
        context.application.create_task(_delete_finished_battle(context, msg.chat_id, old_message_id))
    await reply_and_expire(msg, context, "🛑 Tree Battle ကို ပယ်ဖျက်လိုက်ပါပြီ။ နောက်ပွဲအသစ် စနိုင်ပါပြီ။")
