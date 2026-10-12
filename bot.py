

# ===============================
# TAROT CARD MEANING DATABASE
# ===============================

tarot_meaning = {

"The Fool":
"🌱 အသစ်စတင်မှု\nအခွင့်အရေးအသစ်တွေ ရလာနိုင်ပါတယ်။\nအလျင်စလို မလုပ်ဘဲ စဉ်းစားပါ။",

"The Magician":
"✨ အရည်အချင်းနဲ့ အခွင့်အရေးကို အသုံးချရမယ့်အချိန်ပါ။\nကိုယ့်ရဲ့စွမ်းအားကို ယုံကြည်ပါ။",

"The High Priestess":
"🌙 အတွင်းစိတ်အသံကို နားထောင်ပါ။\nလျှို့ဝှက်ချက်တစ်ခု သိလာနိုင်ပါတယ်။",

"The Empress":
"🌸 အောင်မြင်မှုနဲ့ ကြီးပွားမှု ရလာနိုင်ပါတယ်။",

"The Emperor":
"👑 စည်းကမ်းနဲ့ ဆုံးဖြတ်ချက်က အရေးကြီးပါတယ်။",

"The Lovers":
"❤️ ချစ်ခြင်းနဲ့ ဆက်ဆံရေးပိုင်းမှာ အရေးကြီးတဲ့ရွေးချယ်မှုရှိနိုင်ပါတယ်။",

"The Chariot":
"🏇 ကြိုးစားမှုနဲ့ အောင်မြင်မှုရနိုင်ပါတယ်။",

"The Strength":
"🦁 စိတ်ခွန်အားနဲ့ ပြဿနာတွေကို ကျော်ဖြတ်နိုင်ပါတယ်။",

"The Hermit":
"🕯️ တစ်ယောက်တည်း စဉ်းစားပြီး အဖြေရှာရမယ့်အချိန်ပါ။",

"The Wheel of Fortune":
"🎡 ကံကြမ္မာအပြောင်းအလဲကောင်းတွေ ရှိလာနိုင်ပါတယ်။",

"The Justice":
"⚖️ တရားမျှတမှုနဲ့ မှန်ကန်တဲ့ဆုံးဖြတ်ချက် လိုအပ်ပါတယ်။",

"The Death":
"🦋 အဟောင်းတွေ ပြီးဆုံးပြီး အသစ်စတင်နိုင်ပါတယ်။",

"The Devil":
"😈 သွေးဆောင်မှုတွေကို သတိထားပါ။",

"The Tower":
"⚡ မမျှော်လင့်ထားတဲ့ အပြောင်းအလဲ ဖြစ်နိုင်ပါတယ်။",

"The Star":
"⭐ မျှော်လင့်ချက်နဲ့ ကံကောင်းခြင်း ရှိပါတယ်။",

"The Moon":
"🌙 မသေချာမှုတွေရှိနိုင်လို့ သေချာစဉ်းစားပါ။",

"The Sun":
"☀️ ပျော်ရွှင်မှုနဲ့ အောင်မြင်မှု ရလာနိုင်ပါတယ်။",

"The Judgement":
"🔔 အရေးကြီးတဲ့ ဆုံးဖြတ်ချက်ချရမယ့်အချိန်ပါ။",

"The World":
"🌍 ပြီးမြောက်မှုနဲ့ အောင်မြင်မှုရနိုင်ပါတယ်။"

}

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.helpers import mention_html
from telegram.ext import MessageHandler, filters

from mafia_game import (
    mafia_command,
    mafia_callback,
    mafia_stop_command,
    set_db_pool,
)

from tree_battle import treebattle_command, treebattle_callback, treebattle_cancel_command, set_db_pool as set_tree_battle_db_pool

from game_cleanup import hide_command, schedule_delete, reply_and_expire
from bu_gyi import (
    bu_gyi_command,
    bu_gyi_join_command,
    bu_gyi_bet_command,
    bu_gyi_deal_command,
    bu_gyi_callback,
    set_db_pool as set_bu_gyi_db_pool,
)


import asyncio
from tarot_database import tarot_cards
import random

tarot_readings = {
    "The Magician 🪄": [
        "✨ အစပြုနိုင်စွမ်း၊ ဖန်တီးနိုင်စွမ်းကို ပြသတဲ့ကတ်ပါ။",
        "💫 အခွင့်အရေးအသစ်တွေ ရလာနိုင်ပါတယ်။",
        "🔥 ကိုယ့်ရဲ့ကျွမ်းကျင်မှုကို အသုံးချပါ။"
    ],

    "The Hermit 🕯": [
        "🌙 တိတ်ဆိတ်ပြီး ကိုယ့်ကိုယ်ကို ပြန်လည်ရှာဖွေရမယ့်အချိန်ပါ။",
        "✨ အတွေးအမြင်အသစ်တွေ ရလာနိုင်ပါတယ်။",
        "💫 အလျင်မလိုဘဲ ဆုံးဖြတ်ပါ။"
    ],

    "The World 🌎": [
        "🌟 အောင်မြင်မှုနဲ့ ပြီးမြောက်ခြင်းကို ဆိုလိုပါတယ်။",
        "✨ ခရီးအသစ်တစ်ခု စတင်ဖို့ အချိန်ကောင်းပါ။",
        "💎 ကြိုးစားမှုရဲ့ ရလဒ်ကို ရရှိနိုင်ပါတယ်။"
    ],

    "The Moon 🌙": [
        "🌙 မသေချာမှုတွေ ရှိနိုင်ပေမယ့် အတွင်းစိတ်ကို ယုံကြည်ပါ။",
        "✨ လျှို့ဝှက်ထားတဲ့အရာတွေ ပေါ်လာနိုင်ပါတယ်။"
    ],

    "The Sun ☀️": [
        "☀️ ပျော်ရွှင်မှုနဲ့ အောင်မြင်မှုကို ကိုယ်စားပြုပါတယ်။",
        "✨ အကောင်းဆုံးအချိန်တွေ ရောက်လာနိုင်ပါတယ်။"
    ],

    "Wheel of Fortune 🎡": [
        "🎡 အပြောင်းအလဲနဲ့ ကံကောင်းခြင်းကို ကိုယ်စားပြုပါတယ်။",
        "✨ မမျှော်လင့်ထားတဲ့ အခွင့်အရေးတွေ ရလာနိုင်ပါတယ်။",
        "🌟 ဘဝလမ်းကြောင်းအသစ်တွေ ဖွင့်လာနိုင်ပါတယ်။"
    ]
}

import os

OWNER_ID = 7876735389
import logging
import asyncpg

from dotenv import load_dotenv
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    ChatMemberHandler,
)
from telegram.error import TelegramError

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")
GROUP_ID = -1003788273073
GROUP_INVITE_LINK = "https://t.me/+acEIjbkJWDtmYzc1"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)

db_pool = None


# =========================
# DATABASE
# =========================

async def init_db():
    global db_pool

    db_pool = await asyncpg.create_pool(
        DATABASE_URL,
        min_size=2,
        max_size=10,
        command_timeout=30,
    )

    async with db_pool.acquire() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                telegram_id BIGINT PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                coins BIGINT NOT NULL DEFAULT 0 CHECK (coins >= 0),
                registered_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            );
        """)
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS group_tarot (
               group_id BIGINT PRIMARY KEY,
               count INTEGER DEFAULT 0,
               active BOOLEAN DEFAULT FALSE,
            last_user_id BIGINT,
            last_username TEXT
            );
        """)
        await conn.execute("""
        CREATE TABLE IF NOT EXISTS game_history (
            id BIGSERIAL PRIMARY KEY,
            telegram_id BIGINT NOT NULL,
            chat_id BIGINT,
            bet BIGINT NOT NULL,
            multiplier NUMERIC(4, 2) NOT NULL,
            payout BIGINT NOT NULL,
            balance_after BIGINT NOT NULL,
            played_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            )
        """)


        await conn.execute("""
            CREATE TABLE IF NOT EXISTS coin_gifts (
                id BIGSERIAL PRIMARY KEY,
                chat_id BIGINT NOT NULL,
                message_id BIGINT,
                creator_id BIGINT NOT NULL,
                total_amount BIGINT NOT NULL CHECK (total_amount > 0),
                slots INTEGER NOT NULL CHECK (slots > 0),
                per_person BIGINT NOT NULL CHECK (per_person > 0),
                claimed_count INTEGER NOT NULL DEFAULT 0,
                status TEXT NOT NULL DEFAULT 'open',
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            )
        """)
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS coin_gift_claims (
                gift_id BIGINT NOT NULL REFERENCES coin_gifts(id) ON DELETE CASCADE,
                user_id BIGINT NOT NULL,
                claimed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                PRIMARY KEY (gift_id, user_id)
            )
        """)
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS group_members (
                chat_id BIGINT NOT NULL,
                user_id BIGINT NOT NULL,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                last_seen TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                PRIMARY KEY (chat_id, user_id)
            )
        """)

    logger.info("Database initialized successfully.")


# =========================
# START
# =========================






# ==============================
# GROUP ADMIN /ALL MENTION FEATURE
# ==============================

async def _is_group_admin(update, context):
    """Return True only when the command sender is a group admin/owner."""
    chat = update.effective_chat
    user = update.effective_user
    if not chat or chat.type not in ("group", "supergroup") or not user:
        return False
    try:
        member = await context.bot.get_chat_member(chat.id, user.id)
        return member.status in ("administrator", "creator")
    except TelegramError as exc:
        logger.warning("Admin check failed in %s for %s: %s", chat.id, user.id, exc)
        return False


async def _is_bot_admin(context, chat_id):
    """Return True only when this bot has admin rights in the group."""
    try:
        bot_user = await context.bot.get_me()
        member = await context.bot.get_chat_member(chat_id, bot_user.id)
        return member.status in ("administrator", "creator")
    except TelegramError as exc:
        logger.warning("Bot admin check failed in %s: %s", chat_id, exc)
        return False


async def track_group_member(update, context):
    """Remember human members the bot has seen in each group.

    Telegram Bot API cannot enumerate every ordinary member of a group on demand,
    so /all uses members the bot has observed plus the current administrators.
    """
    message = update.effective_message
    chat = update.effective_chat
    user = update.effective_user
    if not message or not chat or chat.type not in ("group", "supergroup"):
        return
    if not user or getattr(user, "is_bot", False) or db_pool is None:
        return
    try:
        async with db_pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO group_members
                    (chat_id, user_id, username, first_name, last_name, last_seen)
                VALUES ($1, $2, $3, $4, $5, NOW())
                ON CONFLICT (chat_id, user_id) DO UPDATE SET
                    username = EXCLUDED.username,
                    first_name = EXCLUDED.first_name,
                    last_name = EXCLUDED.last_name,
                    last_seen = NOW()
                """,
                chat.id, user.id, user.username, user.first_name, user.last_name,
            )
    except Exception as exc:
        logger.warning("Could not track group member %s in %s: %s", user.id, chat.id, exc)


async def all_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mention all currently known human members in the current group."""
    message = update.effective_message
    chat = update.effective_chat
    if not message or not chat or chat.type not in ("group", "supergroup"):
        if message:
            await message.reply_text("⚠️ /all ကို Group ထဲမှာပဲ အသုံးပြုနိုင်ပါတယ်။")
        return

    if not await _is_group_admin(update, context):
        await message.reply_text("⛔ Group Admin တွေပဲ /all ကို အသုံးပြုနိုင်ပါတယ်။")
        return

    if not await _is_bot_admin(context, chat.id):
        await message.reply_text("⚠️ ဒီ Group မှာ Bot ကို Admin ပေးထားမှ /all အသုံးပြုနိုင်ပါတယ်။")
        return

    text = " ".join(context.args).strip()
    if not text:
        await message.reply_text(
            "အသုံးပြုပုံ — /all အနောက်မှာ ခေါ်ချင်တဲ့စာသားရေးပါ။\n"
            "ဥပမာ — /all အားလုံး ဒီစာကိုဖတ်ပေးပါ"
        )
        return

    jobs = context.application.bot_data.setdefault("all_mention_jobs", {})
    old_job = jobs.get(chat.id)
    if old_job and not old_job.done():
        old_job.cancel()

    # Refresh all administrators (the Bot API exposes this complete list).
    try:
        admins = await context.bot.get_chat_administrators(chat.id)
        async with db_pool.acquire() as conn:
            for admin in admins:
                u = admin.user
                if getattr(u, "is_bot", False):
                    continue
                await conn.execute(
                    """
                    INSERT INTO group_members
                        (chat_id, user_id, username, first_name, last_name, last_seen)
                    VALUES ($1, $2, $3, $4, $5, NOW())
                    ON CONFLICT (chat_id, user_id) DO UPDATE SET
                        username = EXCLUDED.username,
                        first_name = EXCLUDED.first_name,
                        last_name = EXCLUDED.last_name,
                        last_seen = NOW()
                    """,
                    chat.id, u.id, u.username, u.first_name, u.last_name,
                )
    except TelegramError as exc:
        logger.warning("Could not refresh group admins for /all in %s: %s", chat.id, exc)

    async def run_all_mentions():
        try:
            async with db_pool.acquire() as conn:
                rows = await conn.fetch(
                    """
                    SELECT user_id, username, first_name, last_name
                    FROM group_members
                    WHERE chat_id = $1
                    ORDER BY last_seen DESC, user_id
                    """,
                    chat.id,
                )

            if not rows:
                await message.reply_text("⚠️ Bot က ဒီ Group ထဲက member တစ်ယောက်မှ မတွေ့ရသေးပါ။")
                return

            from html import escape
            safe_text = escape(text)
            prefix = f"📢 <b>{safe_text}</b>\n\n"
            chunk = prefix
            sent = 0

            for row in rows:
                display = (row["first_name"] or "Member").strip()
                if row["last_name"]:
                    display = f"{display} {row['last_name']}".strip()
                mention = mention_html(int(row["user_id"]), display)
                piece = mention + " "

                if len(chunk) + len(piece) > 3500 and chunk != prefix:
                    await context.bot.send_message(
                        chat_id=chat.id,
                        text=chunk,
                        parse_mode="HTML",
                    )
                    sent += 1
                    await asyncio.sleep(0.8)
                    chunk = piece
                else:
                    chunk += piece

            if chunk.strip():
                await context.bot.send_message(
                    chat_id=chat.id,
                    text=chunk,
                    parse_mode="HTML",
                )
                sent += 1

            logger.info("/all completed in %s: %s messages", chat.id, sent)
        except asyncio.CancelledError:
            logger.info("/all stopped in %s", chat.id)
            raise
        except TelegramError as exc:
            logger.warning("/all Telegram error in %s: %s", chat.id, exc)
        finally:
            current = jobs.get(chat.id)
            if current is asyncio.current_task():
                jobs.pop(chat.id, None)

    jobs[chat.id] = asyncio.create_task(run_all_mentions())
    await message.reply_text("📢 /all mention စတင်ပါပြီ။ ရပ်ချင်ရင် /stop ကိုသုံးပါ။")


async def stop_all_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Stop the current /all mention job for this group."""
    message = update.effective_message
    chat = update.effective_chat
    if not message or not chat or chat.type not in ("group", "supergroup"):
        return

    if not await _is_group_admin(update, context):
        await message.reply_text("⛔ Group Admin တွေပဲ /stop ကို အသုံးပြုနိုင်ပါတယ်။")
        return

    if not await _is_bot_admin(context, chat.id):
        await message.reply_text("⚠️ ဒီ Group မှာ Bot ကို Admin ပေးထားမှ /stop အသုံးပြုနိုင်ပါတယ်။")
        return

    jobs = context.application.bot_data.setdefault("all_mention_jobs", {})
    job = jobs.get(chat.id)
    if job and not job.done():
        job.cancel()
        jobs.pop(chat.id, None)
        await message.reply_text("🛑 Member mention လုပ်နေမှုကို ရပ်လိုက်ပါပြီ။")
    else:
        await message.reply_text("ℹ️ လက်ရှိ /all mention လုပ်နေတဲ့ process မရှိပါ။")


# ==============================
# GROUP TAROT EVENT COUNTER
# ==============================


async def group_tarot_counter(update, context):

    if not update.message:
        return

    if update.effective_chat.type not in ["group", "supergroup"]:
        return

    chat_id = update.effective_chat.id

    if 'group_tarot_count' not in context.application.bot_data:
        context.application.bot_data['group_tarot_count'] = {}

    if chat_id not in context.application.bot_data['group_tarot_count']:
        context.application.bot_data['group_tarot_count'][chat_id] = 0

    context.application.bot_data['group_tarot_count'][chat_id] += 1

    count = context.application.bot_data['group_tarot_count'][chat_id]

    if count >= 30:

        context.application.bot_data['group_tarot_count'][chat_id] = 0

        keyboard = [
            [
                InlineKeyboardButton(
                    "🔮 Tarot ကြည့်မယ်",
                    callback_data="group_tarot"
                )
            ]
        ]

        ready_msg = await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="🔮 Tarot Ready\n\n၃၀ စက္ကန့်အတွင်း Tarot ကြည့်ရန် နှိပ်ပါ👇",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        async def delete_ready():
            await asyncio.sleep(30)
            try:
                await ready_msg.delete()
            except Exception:
                pass

        asyncio.create_task(delete_ready())



async def group_tarot_callback(update, context):

    query = update.callback_query
    try:
       await query.answer()
    except TelegramError as e:
       logger.warning("Callback query expired: %s", e)

    # Register check before Tarot
    try:
        async with db_pool.acquire() as conn:
            registered = await conn.fetchrow(
                """
                SELECT telegram_id
                FROM users
                WHERE telegram_id=$1
                """,
                query.from_user.id
            )

        if not registered:
            keyboard = [
                [
                    InlineKeyboardButton(
                        "📝 Register",
                        url=f"https://t.me/{context.bot.username}?start=register"
                    )
                ]
            ]

            await query.message.reply_text(
                "⚠️ Tarot အသုံးပြုရန် Register အရင်လုပ်ပေးပါ။",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            return

    except Exception as e:
        print("Register Check Error:", e)

    try:
        await query.message.delete()
    except:
        pass

    import random
    import os
    from tarot_database import tarot_cards

    user = query.from_user

    # lock first click
    if 'group_tarot_done' not in context.application.bot_data:
        context.application.bot_data['group_tarot_done'] = {}

    chat_id = query.message.chat.id

    if context.application.bot_data['group_tarot_done'].get(chat_id):
        await query.answer(
            "ဒီကဒ်ကို ရယူပြီးပါပြီ။",
            show_alert=True
        )
        return

    context.application.bot_data['group_tarot_done'][chat_id] = True


    # choose tarot card from database
    card_name = random.choice(list(tarot_cards.keys()))

    # random fortune
    fortune = random.choice(
        tarot_cards[card_name]
    )

    # choose image from cards folder
    card_files = [
        "cards/" + f
        for f in os.listdir("cards")
        if f.lower().endswith((".jpg",".png",".jpeg"))
    ]

    card_file = random.choice(card_files)


    # add coin +10

    try:
        async with db_pool.acquire() as conn:
            await conn.execute(
                """
                UPDATE users
                SET coins = coins + 100
                WHERE telegram_id=$1
                """,
                user.id
            )
    except Exception as e:
        print(e)


    username = (
        f"@{user.username}"
        if user.username
        else user.first_name
    )


    caption = (
        "🔮✨ Group Tarot Result ✨🔮\n\n"
        f"👤 Card Owner:\n{username}\n\n"
        f"🃏 Card:\n{card_name}\n\n"
        f"🌙 ဟောစာတမ်း:\n{fortune}\n\n"
        "🎁 Reward:\n+100 Coins"
    )


    photo = open(card_file,"rb")

    msg = await context.bot.send_photo(
        chat_id=chat_id,
        photo=photo,
        caption=caption
    )

    photo.close()


    await asyncio.sleep(60)


    try:
        await msg.delete()
    except:
        pass


    # reset
    context.application.bot_data['group_tarot_done'][chat_id] = False


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    async with db_pool.acquire() as conn:
        existing_user = await conn.fetchrow(
            "SELECT coins FROM users WHERE telegram_id=$1",
            user.id
        )

    if existing_user:

        coins = existing_user["coins"]

        await update.message.reply_text(
            "🔮 မင်္ဂလာပါ " + user.first_name + "!\n\n"
            "🃏 MyCard Fortune Bot မှ ကြိုဆိုပါတယ်။\n\n"
            "💰 လက်ကျန် Coins: " + str(coins) + "\n\n"
            "အသုံးပြုနိုင်သော Commands:\n"
            "/mycard - 🔮 Card Reading\n"
            "/game - 🎮 Daily Game\n"
            "/mafia - 🕵 Mafia Game\n"
            "/dailycoin - 💰 Daily Coin\n"
            "/mycoin - 💰 မိမိပိုင်ဆိုင်သော Coin များ\n"
            "/give username amount - 🎁 Member ကို Coin ပေးရန်\n"
            "ဥပမာ: /give @username 10000\n"
            "/rank - 👑 Global Coin Top 10\n"
            "/help - 📖 Help"
        )

    else:

        keyboard = [
            [
                InlineKeyboardButton(
                    "📝 Register",
                    callback_data="register"
                )
            ]
        ]

        await update.message.reply_text(
            "🔮 မင်္ဂလာပါ!\n\n"
            "🃏 MyCard Fortune Bot မှ ကြိုဆိုပါတယ်။\n\n"
            "အသုံးပြုရန် Register လုပ်ပါ။",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

async def tarot_callback(update, context):
    query = update.callback_query
    await query.answer()

    # Button နှိပ်လိုက်တာနဲ့ /mycard menu စာသားနှင့် button ကိုပါ ဖျက်ပါ
    try:
        await query.message.delete()
    except Exception:
        pass

    data = query.data

    costs = {
        "card_1": 100,
        "card_3": 250,
        "card_5": 400
    }

    cost = costs.get(data)

    if not cost:
        return

    user_id = query.from_user.id

    # check user coin
    row = await db_pool.fetchrow(
        "SELECT coins FROM users WHERE telegram_id=$1",
        user_id
    )

    if not row or row["coins"] < cost:
        coins = row["coins"] if row else 0

        await context.bot.send_message(
            chat_id=query.message.chat.id,
            text=(
                "🔮 Tarot Reading မရသေးပါ ✨\n\n"
                "❌ Coin မလောက်သေးပါ\n\n"
                "💰 လိုအပ်သော Coin : " + str(cost) + "\n"
                "💎 လက်ရှိ Coin : " + str(coins) + "\n\n"
                "━━━━━━━━━━━━━━\n"
                "💳 Coin ဝယ်ယူရန် ဆက်သွယ်ပါ\n"
                "👑 Owner : @helixdemo\n\n"
                "🎮 Daily Game ကစားပြီး Coin ရယူနိုင်ပါတယ် ✨"
            )
        )
        return

# remove coin
    await db_pool.execute(
        "UPDATE users SET coins = coins - $1 WHERE telegram_id=$2",
        cost,
        user_id
    )

    import random

    cards = [
("The Fool 🃏", "cards/00_Fool.jpg"),
("The Magician 🪄", "cards/01_Magician.jpg"),
("The High Priestess 🌙", "cards/02_High_Priestess.jpg"),
("The Empress 👑", "cards/03_Empress.jpg"),
("The Emperor 👑", "cards/04_Emperor.jpg"),
("The Hierophant 📜", "cards/05_Hierophant.jpg"),
("The Lovers ❤️", "cards/06_Lovers.jpg"),
("The Chariot 🛡️", "cards/07_Chariot.jpg"),
("The Strength 💪", "cards/08_Strength.jpg"),
("The Hermit 🕯️", "cards/09_Hermit.jpg"),
("Wheel of Fortune 🎡", "cards/10_Wheel_of_Fortune.jpg"),
("Justice ⚖️", "cards/11_Justice.jpg"),
("The Hanged Man 🙃", "cards/12_Hanged_Man.jpg"),
("Death 💀", "cards/13_Death.jpg"),
("Temperance 🕊️", "cards/14_Temperance.jpg"),
("The Devil 😈", "cards/15_Devil.jpg"),
("The Tower ⚡", "cards/16_Tower.jpg"),
("The Star ⭐", "cards/17_Star.jpg"),
("The Moon 🌙", "cards/18_Moon.jpg"),
("The Sun ☀️", "cards/19_Sun.jpg"),
("Judgement 🔔", "cards/20_Judgement.jpg"),
("The World 🌎", "cards/21_World.jpg")
]

    count = int(data.split("_")[1])

    result = random.sample(cards, count)

    for name, image in result:

        loading = await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="🔮 Tarot Energy Loading...\n\n✨✨✨\n\n🃏 Card Drawing..."
        )

        await asyncio.sleep(0.2)

        effects = [
            "🌙 စကြဝဠာစွမ်းအင်များနှင့် ချိတ်ဆက်နေပါသည်...",
            "✨ ရှေးဟောင်း Tarot ကတ်များကို ရောမွှေနေပါသည်...",
            "🔮 သင့်ကံကြမ္မာအဖြေများကို ဖတ်ရှုနေပါသည်...",
            "🌌 အနာဂတ်လမ်းကြောင်းများကို ရှာဖွေနေပါသည်...",
            "💫 သင့်အတွက် အထူးကတ်ကို ရွေးချယ်နေပါသည်...",
            "🔥 ကံကြမ္မာတံခါးကို ဖွင့်လှစ်နေပါသည်..."
        ]

        for i in range(1, 7):
            await loading.edit_text(
                f"{effects[i-1]}\n\n"
                f"🃏 Tarot Card Shuffle အဆင့် {i}/6 🔄\n\n"
                "✨ ခဏစောင့်ပါ... သင့်ကံကြမ္မာကို ဖော်ထုတ်နေပါသည်..."
            )
            await asyncio.sleep(0.15)

        await loading.edit_text(
            "🔥 Destiny Card Found!\n\n✨ Preparing your result..."
        )

        await asyncio.sleep(0.2)

        cards = tarot_cards.get(name)

        if not cards:
            cards= [
                "✨ သင့်အတွက် အခွင့်အရေးအသစ်တွေ ရှိလာနိုင်ပါတယ်။",
                "🌙 စိတ်ရှည်ပြီး ဆုံးဖြတ်ချက်ကောင်းတွေ ချပါ။",
                "🔥 ယုံကြည်မှုနဲ့ ရှေ့ဆက်ပါ။"
            ]

    username = query.from_user.username

    if username:
        user_tag = f"@{username}"
    else:
        user_tag = query.from_user.first_name

    reading = (
        "🔮✨ MYCARD TAROT RESULT ✨🔮\n\n"
        f"👤 Reader: {user_tag}\n\n"
        f"🎴 {name}\n\n"
        "━━━━━━━━━━━━━━\n\n"
        "🌙 Card Meaning:\n\n"
        + "\n".join(random.sample(cards, min(5, len(cards))))
        + "\n\n━━━━━━━━━━━━━━\n\n"
        "💎 Universe Message:\n"
        "✨ သင့်အတွက် ကောင်းမွန်သော အခွင့်အရေးများ ရောက်ရှိလာနိုင်ပါသည်။\n\n"
        "🌙 Thank you for using MyCard"
        )

    await loading.delete()

    # ရလဒ်စာသားနဲ့ တူညီတဲ့ ရွေးထားသောကတ်ပုံကို အသုံးပြုပါ
    card_file = image if isinstance(image, str) else 'cards/00_Fool.jpg'

    with open(card_file, "rb") as card_image:
        result_message = await context.bot.send_photo(
            chat_id=query.message.chat.id,
            photo=card_image,
            caption=reading
        )

    # Tarot ရလဒ် (ပုံနှင့်စာသား) ကို 30 စက္ကန့်ကြာပြီးမှ ဖျက်ပါ
    asyncio.create_task(
        delete_message_after(
            context,
            result_message.chat_id,
            result_message.message_id,
            30
        )
    )


# ==============================
# Premium Tarot Typing Effect
# Card ပေါ်ပြီး စာတန်းရေးသလို Effect
# ==============================






async def addcoin_command(update, context):
    if update.effective_user.id != OWNER_ID:
        return

    if len(context.args)<2:
        return await update.message.reply_text(
            "❌ /addcoin USER_ID AMOUNT"
        )

    user_id=int(context.args[0])
    amount=int(context.args[1])

    conn=await asyncpg.connect(os.getenv("DATABASE_URL"))

    row=await conn.fetchrow(
        "SELECT coins FROM users WHERE telegram_id=$1",
        user_id
    )

    if not row:
        await conn.close()
        return await update.message.reply_text("❌ User မရှိပါ")

    await conn.execute(
        "UPDATE users SET coins=coins+$1 WHERE telegram_id=$2",
        amount,
        user_id
    )

    new_coin=row["coins"]+amount

    await conn.close()

    await update.message.reply_text(
        f"✅ Coin ထည့်ပြီးပါပြီ\n\n"
        f"👤 User ID: {user_id}\n"
        f"💰 +{amount} Coins\n"
        f"💎 Total: {new_coin}"
    )

    try:
        await context.bot.send_message(
            chat_id=user_id,
            text=f"Coin received!\n+{amount} Coins\nTotal: {new_coin}"
        )
    except Exception as e:
        print(e)


async def coin_command(update, context):
    if update.effective_user.id != OWNER_ID:
        return

    if not context.args:
        return

    user_id = int(context.args[0])

    conn = await asyncpg.connect(os.getenv("DATABASE_URL"))

    row = await conn.fetchrow(
        "SELECT coins FROM users WHERE telegram_id=$1",
        user_id
    )

    await conn.close()

    if row:
        await update.message.reply_text(
            f"💰 User Coin\n\nID: {user_id}\nCoins: {row["coins"]}"
        )
    else:
        await update.message.reply_text("❌ User မတွေ့ပါ")


# ===============================
# OWNER ONLY: TAKE COINS BACK
# ===============================
async def takecoin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_user or update.effective_user.id != OWNER_ID:
        return

    if len(context.args) != 2:
        await update.message.reply_text(
            "အသုံးပြုပုံ: /takecoin USER_ID AMOUNT\n"
            "ဥပမာ: /takecoin 123456789 100"
        )
        return

    try:
        user_id = int(context.args[0])
        amount = int(context.args[1])
    except ValueError:
        await update.message.reply_text("❌ User ID နဲ့ Coin ပမာဏကို နံပါတ်ဖြင့် ထည့်ပါ။")
        return

    if user_id <= 0 or amount <= 0:
        await update.message.reply_text("❌ User ID နဲ့ Coin ပမာဏသည် 0 ထက်ကြီးရပါမယ်။")
        return

    async with db_pool.acquire() as conn:
        async with conn.transaction():
            row = await conn.fetchrow(
                "SELECT coins FROM users WHERE telegram_id=$1 FOR UPDATE",
                user_id,
            )
            if not row:
                await update.message.reply_text("❌ Register လုပ်ထားတဲ့ User မတွေ့ပါ။")
                return
            balance = int(row["coins"])
            if amount > balance:
                await update.message.reply_text(
                    f"❌ User ရဲ့ လက်ကျန် Coin က {balance:,} ပဲရှိပါတယ်။"
                )
                return
            new_balance = balance - amount
            await conn.execute(
                "UPDATE users SET coins=$1, updated_at=NOW() WHERE telegram_id=$2",
                new_balance,
                user_id,
            )

    await update.message.reply_text(
        "✅ Coin ပြန်သိမ်းပြီးပါပြီ။\n\n"
        f"👤 User ID: {user_id}\n"
        f"➖ သိမ်းယူမှု: {amount:,} Coins\n"
        f"💰 လက်ကျန်: {new_balance:,} Coins"
    )
    try:
        await context.bot.send_message(
            chat_id=user_id,
            text=(
                "ℹ️ သင့်အကောင့်မှ Coin ကို Owner မှ ပြန်လည်သိမ်းယူထားပါတယ်။\n"
                f"➖ သိမ်းယူမှု: {amount:,} Coins\n"
                f"💰 လက်ကျန်: {new_balance:,} Coins"
            ),
        )
    except Exception as e:
        logger.info("Could not notify user %s about coin adjustment: %s", user_id, e)


async def takeallcoins_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_user or update.effective_user.id != OWNER_ID:
        return

    if not context.args or context.args[0] != "CONFIRM":
        await update.message.reply_text(
            "⚠️ Register လုပ်ထားသူအားလုံးရဲ့ Coin ကို 0 ပြန်ထားမယ့် လုပ်ဆောင်ချက်ပါ။\n"
            "အတည်ပြုရန်: /takeallcoins CONFIRM"
        )
        return

    async with db_pool.acquire() as conn:
        rows = await conn.fetch(
            "UPDATE users SET coins=0, updated_at=NOW() WHERE coins > 0 "
            "RETURNING telegram_id, coins"
        )

    await update.message.reply_text(
        "✅ Register လုပ်ထားသူအားလုံးရဲ့ Coin ကို 0 ပြန်ထားပြီးပါပြီ။\n"
        f"👥 Coin ပြောင်းလဲထားသော User: {len(rows)} ဦး"
    )


async def mycoin_command(update, context):
    user_id = update.effective_user.id

    conn = await asyncpg.connect(os.getenv("DATABASE_URL"))

    row = await conn.fetchrow(
        "SELECT coins FROM users WHERE telegram_id=$1",
        user_id
    )

    await conn.close()

    if row:
        await update.message.reply_text(
            "💰 My Coin Balance"
            f"👤 User: {update.effective_user.first_name}"
            f"🪙 Coins: {row['coins']}"
            "🔮 Tarot Card ကြည့်နိုင်ပါသည်"
        )
    else:
        await update.message.reply_text(
            "❌ Register မလုပ်ရသေးပါ/start နှိပ်ပါ"
        )


async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.message.reply_text(
        "📖 MyCard Fortune Bot Help\n\n"
        "/start - Bot စတင်ရန်\n"
        "/help - အကူအညီ\n"
        "/mycard - 🔮 သင့်ကံကြမာကြည့်ရန်\n"
        "/dailycoin - တစ်နေ့တစ်ခါရယူရန်\n"
        "/mycoin - 💰 coinစစ်ရန်\n"
        "/give username amount - 🎁 Member ကို Coin ပေးရန်\n"
        "ဥပမာ: /give @username 10000\n"
        "/game - 🎮 Daily Game\n"
        "/mafia - 🕵️ Mafia Game\n"
        "/rank - 👑 Global Coin Top 10 (အဆင့်သတ်မှတ်ခြင်း)"
    )


# =========================
# PLACEHOLDER COMMANDS
# =========================

async def mycard_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    # User ရိုက်လိုက်သော /mycard command ကို ချက်ချင်းဖျက်ပါ
    try:
        await update.message.delete()
    except Exception:
        pass

    keyboard = [
        [
            InlineKeyboardButton(
                "🔮 1 Card (100 Coins)",
                callback_data="card_1"
            )
        ],
        
        ]

    prompt_message = await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=(
            "🔮 တာရော့ကြည့်မယ်\n"
            "coin 100 ကုန်ပါမည်"
        ),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    # Menu ကို button နှိပ်သည့်အချိန်တွင် callback က ဖျက်ပေးပါမည်

# ==============================
# ==============================
# MEMBER: GIVE COINS TO ANOTHER REGISTERED MEMBER
# ==============================
async def give_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    """Transfer coins from the command sender to another registered member."""
    sender = update.effective_user
    message = update.effective_message

    if not sender or not message:
        return

    if len(context.args) != 2:
        await message.reply_text(
            "🎁 Coin ပေးရန် အသုံးပြုပုံ\n\n"
            "/give username amount\n\n"
            "ဥပမာ: /give @username 10000\n"
            "💡 @ မပါဘဲ username နဲ့လည်း ရိုက်နိုင်ပါတယ်။"
        )
        return

    username = context.args[0].strip().lstrip("@").strip()
    try:
        amount = int(context.args[1].replace(",", "").strip())
    except ValueError:
        await message.reply_text(
            "❌ Coin ပမာဏကို နံပါတ်ဖြင့် ထည့်ပါ။\n"
            "ဥပမာ: /give @username 10000"
        )
        return

    if not username or amount <= 0:
        await message.reply_text(
            "❌ Username မှန်မှန်နဲ့ Coin ပမာဏကို 0 ထက်ကြီးအောင် ထည့်ပါ။"
        )
        return

    if sender.username and sender.username.lower() == username.lower():
        await message.reply_text("❌ ကိုယ့်ကိုယ်ကို Coin ပြန်ပေးလို့မရပါ။")
        return

    sender_display = f"@{sender.username}" if sender.username else sender.full_name

    async with db_pool.acquire() as conn:
        async with conn.transaction():
            recipient = await conn.fetchrow(
                """
                SELECT telegram_id, username, first_name, coins
                FROM users
                WHERE username IS NOT NULL
                  AND LOWER(username) = LOWER($1)
                FOR UPDATE
                """,
                username,
            )

            if not recipient:
                await message.reply_text(
                    f"❌ @{username} ကို Register လုပ်ထားတဲ့ Member အဖြစ် မတွေ့ပါ။\n"
                    "💡 လက်ခံသူက Bot မှာ /start → Register အရင်လုပ်ထားရပါမယ်။"
                )
                return

            if int(recipient["telegram_id"]) == int(sender.id):
                await message.reply_text("❌ ကိုယ့်ကိုယ်ကို Coin ပြန်ပေးလို့မရပါ။")
                return

            sender_row = await conn.fetchrow(
                "SELECT coins FROM users WHERE telegram_id=$1 FOR UPDATE",
                sender.id,
            )

            if not sender_row:
                await message.reply_text(
                    "❌ သင်ကိုယ်တိုင် Register မလုပ်ရသေးပါ။\n"
                    "/start ကိုနှိပ်ပြီး Register အရင်လုပ်ပါ။"
                )
                return

            sender_balance = int(sender_row["coins"])
            if sender_balance < amount:
                await message.reply_text(
                    "❌ Coin မလုံလောက်ပါ။\n\n"
                    f"💰 ပေးမည့် Coin: {amount:,}\n"
                    f"💎 သင့်လက်ကျန်: {sender_balance:,}"
                )
                return

            recipient_old = int(recipient["coins"])
            sender_new = sender_balance - amount
            recipient_new = recipient_old + amount

            await conn.execute(
                """
                UPDATE users
                SET coins=$1, updated_at=NOW()
                WHERE telegram_id=$2
                """,
                sender_new,
                sender.id,
            )
            await conn.execute(
                """
                UPDATE users
                SET coins=$1, updated_at=NOW()
                WHERE telegram_id=$2
                """,
                recipient_new,
                recipient["telegram_id"],
            )

    recipient_display = (
        f"@{recipient['username']}"
        if recipient["username"]
        else recipient["first_name"]
    )

    await message.reply_text(
        "✅ Coin ပေးပြီးပါပြီ။\n\n"
        f"👤 ပေးသူ: {sender_display}\n"
        f"🎁 လက်ခံသူ: {recipient_display}\n"
        f"💰 ပေးလိုက်သော Coin: {amount:,}\n"
        f"💎 သင့်လက်ကျန်: {sender_new:,}"
    )

    try:
        await context.bot.send_message(
            chat_id=int(recipient["telegram_id"]),
            text=(
                "🎁 Coin ရရှိပါပြီ။\n\n"
                f"👤 ပေးသူ: {sender_display}\n"
                f"🎁 လက်ခံသူ: {recipient_display}\n"
                f"💰 ရရှိသော Coin: +{amount:,}\n"
                f"💎 လက်ကျန် Coin: {recipient_new:,}"
            ),
        )
    except Exception as e:
        logger.info(
            "Could not notify recipient %s about /give: %s",
            recipient["telegram_id"],
            e,
        )


# OWNER: GIVE COINS TO ALL REGISTERED USERS
# ==============================

async def allcoin_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    if update.effective_user.id != OWNER_ID:
        return

    if not context.args:
        await update.message.reply_text(
            "အသုံးပြုပုံ: /allcoin 100"
        )
        return

    try:
        amount = int(context.args[0])
    except ValueError:
        await update.message.reply_text(
            "❌ Coin ပမာဏကို နံပါတ်ဖြင့် ထည့်ပါ။"
        )
        return

    if amount <= 0:
        await update.message.reply_text(
            "❌ Coin ပမာဏသည် 0 ထက်ကြီးရပါမယ်။"
        )
        return

    sender = update.effective_user
    sender_name = (
        f"@{sender.username}"
        if sender.username
        else sender.full_name
    )

    # Add coins to every registered user
    async with db_pool.acquire() as conn:
        users = await conn.fetch(
            """
            UPDATE users
            SET coins = coins + $1
            RETURNING telegram_id, username, first_name, coins
            """,
            amount
        )

    if not users:
        await update.message.reply_text(
            "❌ Register လုပ်ထားတဲ့ User မရှိသေးပါ။"
        )
        return

    success = 0
    failed = 0

    # Notify each registered user in private chat
    for user in users:
        try:
            await context.bot.send_message(
                chat_id=user["telegram_id"],
                text=(
                    "🎁 မုန့်ဖိုး Coin ရရှိပါပြီ!\n\n"
                    f"👤 ပေးသူ: {sender_name}\n"
                    f"💰 ရရှိသော Coin: +{amount}\n"
                    f"💎 လက်ကျန် Coin: {user['coins']}"
                )
            )
            success += 1
        except Exception as e:
            logger.warning(
                "Could not notify user %s: %s",
                user["telegram_id"],
                e
            )
            failed += 1

    # Announce once in the group
    try:
        await context.bot.send_message(
            chat_id=GROUP_ID,
            text=(
                "🎁 မုန့်ဖိုး Coin ပေးဝေခြင်း\n\n"
                f"👤 ပေးသူ: {sender_name}\n"
                f"💰 User တစ်ယောက်စီ: +{amount} Coins\n"
                f"👥 Register User စုစုပေါင်း: {len(users)} ဦး\n"
                f"✅ Private Message ပို့နိုင်သူ: {success} ဦး\n"
                f"⚠️ Message မပို့နိုင်သူ: {failed} ဦး"
            )
        )
    except Exception as e:
        logger.warning("Allcoin group announcement failed: %s", e)

    await update.message.reply_text(
        "✅ Coin ပေးဝေမှု ပြီးပါပြီ!\n\n"
        f"💰 User တစ်ယောက်စီ: +{amount} Coins\n"
        f"👥 Register User: {len(users)} ဦး\n"
        f"✅ Message ပို့နိုင်သူ: {success} ဦး\n"
        f"⚠️ Message မပို့နိုင်သူ: {failed} ဦး"
    )

async def expire_game_message(context, chat_id, message_id):
    await asyncio.sleep(60)

    pending = context.application.bot_data.get(
        "pending_game_messages", {}
    )

    key = (chat_id, message_id)

    if key in pending:
        pending.pop(key, None)

        try:
            await context.bot.delete_message(
                chat_id=chat_id,
                message_id=message_id
            )
        except Exception as e:
            logger.warning("Game message delete failed: %s", e)


async def game_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    user = update.effective_user
    chat = update.effective_chat
    message = update.effective_message

    if chat is None or message is None:
        return

    context.application.create_task(hide_command(context, message))

    async with db_pool.acquire() as conn:
        registered = await conn.fetchval(
            "SELECT 1 FROM users WHERE telegram_id = $1",
            user.id,
        )

    if not registered:
        await reply_and_expire(message, context, 
            "❌ Register မလုပ်ရသေးပါ။\n"
            "/start ကိုနှိပ်ပြီး Register အရင်လုပ်ပါ။"
        )
        return

    rounds = context.application.bot_data.setdefault(
        "game_rounds", {}
    )

    existing = rounds.get(chat.id)

    if existing and not existing["closed"]:
        await reply_and_expire(message, context, 
            "🎮 ဒီ Chat မှာ Game တစ်ပွဲ လက်ရှိဖွင့်ထားပါတယ်။\n"
            "⏳ အဲဒီပွဲပြီးတဲ့အထိ စောင့်ပေးပါ။"
        )
        return

    keyboard = [
        [
            InlineKeyboardButton(
                "10 Coins",
                callback_data="game_bet:10"
            ),
            InlineKeyboardButton(
                "100 Coins",
                callback_data="game_bet:100"
            ),
            InlineKeyboardButton(
                "1,000 Coins",
                callback_data="game_bet:1000"
            ),
        ],
        [
            InlineKeyboardButton(
                "5,000 Coins",
                callback_data="game_bet:5000"
            ),
            InlineKeyboardButton(
                "10,000 Coins",
                callback_data="game_bet:10000"
            ),
        ],
    ]

    game_image = (
        "https://images.unsplash.com/"
        "photo-1511512578047-dfb367046420"
        "?auto=format&fit=crop&w=1200&q=85"
    )

    caption = (
        "🎮 MyCard Coin Game\n\n"
        "💰 လောင်းကြေးကို ရွေးချယ်ပါ။\n"
        "⏳ လောင်းကြေးလက်ခံချိန် — ၁ မိနစ်\n"
        "👥 ပါဝင်သူ — ၀ ဦး\n\n"
        "👇 အောက်က Button ကိုနှိပ်ပါ။"
    )

    # The /game command is auto-deleted shortly after this handler starts.
    # Send the game panel as a normal message, not as a reply to /game,
    # otherwise Telegram can return "Message to be replied not found".
    game_message = await context.bot.send_photo(
        chat_id=chat.id,
        photo=game_image,
        caption=caption,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

    # Keep the game panel until the round settles; deleting it here races
    # with finish_game_round and can make the result flow unreliable.

    round_state = {
        "message_id": game_message.message_id,
        "chat_id": chat.id,
        "bets": {},
        "lock": asyncio.Lock(),
        "closed": False,
    }

    rounds[chat.id] = round_state

    context.application.create_task(
        finish_game_round(
            context.application,
            chat.id,
            round_state,
        )
    )


async def game_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()

    user = query.from_user
    message = query.message

    if message is None:
        return

    chat_id = message.chat_id
    rounds = context.application.bot_data.get(
        "game_rounds", {}
    )
    round_state = rounds.get(chat_id)

    if (
        not round_state
        or round_state["closed"]
        or round_state["message_id"] != message.message_id
    ):
        await query.answer(
            "⏰ ဒီ Game ပွဲ ပြီးဆုံးသွားပါပြီ။",
            show_alert=True,
        )
        return

    try:
        bet = int(query.data.split(":")[1])
    except (ValueError, IndexError):
        return

    if bet not in [10, 100, 1000, 5000, 10000]:
        return

    async with db_pool.acquire() as conn:
        balance = await conn.fetchval(
            "SELECT coins FROM users WHERE telegram_id = $1",
            user.id,
        )

    if balance is None:
        await query.answer(
            "❌ Register အရင်လုပ်ပါ။",
            show_alert=True,
        )
        return

    if balance < bet:
        await query.answer(
            f"Coin မလုံလောက်ပါ။ လက်ကျန် {balance:,} Coins",
            show_alert=True,
        )
        return

    async with round_state["lock"]:
        if round_state["closed"]:
            await query.answer(
                "⏰ ဒီ Game ပွဲ ပြီးဆုံးသွားပါပြီ။",
                show_alert=True,
            )
            return

        round_state["bets"][user.id] = {
            "name": user.full_name,
            "username": user.username,
            "bet": bet,
        }

        bets = list(round_state["bets"].values())

        lines = []
        for item in bets:
            name = (
                "@" + item["username"]
                if item["username"]
                else item["name"]
            )
            lines.append(
                f"👤 {name} — {item['bet']:,} Coins"
            )

        bet_list = "\n".join(lines)

        new_caption = (
            "🎮 MyCard Coin Game\n\n"
            "💰 လောင်းကြေး လက်ခံနေပါသည်။\n"
            "⏳ စုစုပေါင်းအချိန် — ၁ မိနစ်\n"
            f"👥 ပါဝင်သူ — {len(bets)} ဦး\n\n"
            f"{bet_list}\n\n"
            "👇 လောင်းကြေးပြောင်းလိုပါက Button ထပ်နှိပ်ပါ။"
        )

        try:
            await query.edit_message_caption(
                caption=new_caption,
                reply_markup=message.reply_markup,
            )
        except Exception as e:
            logger.warning(
                "Game caption update failed: %s", e
            )


async def finish_game_round(
    application: Application,
    chat_id: int,
    round_state: dict,
):
    await asyncio.sleep(60)

    async with round_state["lock"]:
        if round_state["closed"]:
            return

        round_state["closed"] = True
        bets = dict(round_state["bets"])

    results = []

    for telegram_id, item in bets.items():
        bet = item["bet"]

        multiplier = random.choices(
            [0, 0.5, 1, 2, 3, 5],
            weights=[40, 15, 5, 33, 5, 2],
            k=1
        )[0]

        payout = int(bet * multiplier)

        try:
            async with db_pool.acquire() as conn:
                async with conn.transaction():
                    row = await conn.fetchrow(
                        "SELECT coins FROM users "
                        "WHERE telegram_id = $1 FOR UPDATE",
                        telegram_id,
                    )

                    if not row or row["coins"] < bet:
                        results.append(
                            f"👤 {item['name']}\n"
                            f"💰 လောင်းကြေး: {bet:,} Coins\n"
                            "❌ လက်ကျန် Coin မလုံလောက်လို့ "
                            "ဒီတစ်ကြိမ် မတွက်ချက်နိုင်ပါ။"
                        )
                        continue

                    new_balance = row["coins"] - bet + payout

                    await conn.execute(
                        "UPDATE users SET coins = $1, "
                        "updated_at = NOW() WHERE telegram_id = $2",
                        new_balance,
                        telegram_id,
                    )

                    await conn.execute(
                        "INSERT INTO game_history "
                        "(telegram_id, chat_id, bet, multiplier, "
                        "payout, balance_after) "
                        "VALUES ($1, $2, $3, $4, $5, $6)",
                        telegram_id,
                        chat_id,
                        bet,
                        multiplier,
                        payout,
                        new_balance,
                    )

            net = payout - bet

            if net > 0:
                status = f"🎉 အနိုင် — +{net:,} Coins"
            elif net < 0:
                status = f"❌ အရှုံး — {abs(net):,} Coins"
            else:
                status = "🤝 အရှုံးအနိုင် မရှိပါ"

            name = (
                "@" + item["username"]
                if item["username"]
                else item["name"]
            )

            results.append(
                f"👤 {name}\n"
                f"💰 လောင်းကြေး: {bet:,} Coins\n"
                f"🎯 Multiplier: {multiplier}x\n"
                f"🏆 ပြန်ရရှိမှု: {payout:,} Coins\n"
                f"{status}\n"
                f"💳 လက်ကျန်: {new_balance:,} Coins"
            )

        except Exception:
            logger.exception(
                "Game settlement failed for user %s",
                telegram_id,
            )
            results.append(
                f"👤 {item['name']}\n"
                "⚠️ ရလဒ်တွက်ချက်ရာတွင် Error ဖြစ်သွားပါသည်။"
            )

    if not results:
        result_text = (
            "🎮 MyCard Game Result\n\n"
            "ဒီတစ်ကြိမ်မှာ ပါဝင်သူ မရှိပါ။"
        )
    else:
        result_text = (
            "🎮 MyCard Game Result\n\n"
            + "\n\n".join(results)
        )

    # Send the result first so it is visible before the old panel is removed.
    result_message = None
    try:
        result_message = await application.bot.send_message(
            chat_id=chat_id,
            text=result_text,
        )
    except Exception as e:
        logger.exception("Game result send failed: %s", e)

    # Remove only the betting panel after the result has been posted.
    try:
        await application.bot.delete_message(
            chat_id=chat_id,
            message_id=round_state["message_id"],
        )
    except Exception as e:
        logger.warning("Game panel delete failed: %s", e)

    # Keep the result visible for a full minute, then remove it.
    if result_message is not None:
        await asyncio.sleep(60)
        try:
            await application.bot.delete_message(
                chat_id=chat_id,
                message_id=result_message.message_id,
            )
        except Exception as e:
            logger.warning("Game result delete failed: %s", e)

    rounds = application.bot_data.get("game_rounds", {})
    if rounds.get(chat_id) is round_state:
        rounds.pop(chat_id, None)




async def dailycoin_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    import random
    from datetime import datetime, timezone

    user = update.effective_user

    async with db_pool.acquire() as conn:
        data = await conn.fetchrow(
            """
            SELECT coins, last_daily_coin
            FROM users
            WHERE telegram_id = $1
            """,
            user.id,
        )

        if not data:
            await update.message.reply_text(
                "❌ အရင်ဆုံး /start လုပ်ပြီး Register လုပ်ပါ"
            )
            return

        now = datetime.now(timezone.utc)

        if data["last_daily_coin"]:
            if data["last_daily_coin"].date() == now.date():
                await update.message.reply_text(
                    "⏳ ဒီနေ့ Daily Coin ယူပြီးပါပြီမနက်ဖြန် ပြန်လာပါ"
                )
                return

        reward = random.randint(10, 100)

        await conn.execute(
            """
            UPDATE users
            SET coins = coins + $1,
                last_daily_coin = $2,
                updated_at = NOW()
            WHERE telegram_id = $3
            """,
            reward,
            now,
            user.id,
        )

        await update.message.reply_text(
            f"💰 Daily Coin ရရှိပါပြီ!"
            f"🎁 +{reward} Coins"
             "မနက်ဖြန် ပြန်ယူနိုင်ပါတယ်"
        )


# =========================

# =========================
# GLOBAL COIN RANKING — TOP 10
# =========================
async def rank_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show the global top 10 registered users by coin balance."""
    message = update.effective_message
    if not message:
        return

    try:
        async with db_pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT telegram_id, username, first_name, coins
                FROM users
                ORDER BY coins DESC, telegram_id ASC
                LIMIT 10
                """
            )
    except Exception as e:
        logger.exception("Global rank query failed: %s", e)
        await message.reply_text(
            "⚠️ Global Rank ကို ယာယီမဖွင့်နိုင်သေးပါ။ ခဏနေပြီး ပြန်စမ်းပါ။"
        )
        return

    if not rows:
        await message.reply_text(
            "🏆 GLOBAL COIN RANKING\n\n"
            "📭 Register လုပ်ထားတဲ့ Member မရှိသေးပါ။"
        )
        return

    def display_name(row):
        if row["username"]:
            return f"@{row['username']}"
        return row["first_name"] or f"User {row['telegram_id']}"

    lines = [
        "👑✨ GLOBAL COIN RANKING ✨👑",
        "━━━━━━━━━━━━━━━━━━━━",
        "🌍 All Registered Members • Top 10",
        "💰 Coin အများဆုံးသူများ",
        "━━━━━━━━━━━━━━━━━━━━",
    ]

    medals = ["🥇", "🥈", "🥉"]
    for index, row in enumerate(rows, start=1):
        name = display_name(row)
        coins = int(row["coins"])
        if index == 1:
            lines.extend([
                "",
                "👑━━━━━━━━━━━━━━━━━━👑",
                f"🏆 GLOBAL NUMBER 1",
                f"👤 {name}",
                f"💎 {coins:,} COINS",
                "👑━━━━━━━━━━━━━━━━━━👑",
            ])
        else:
            icon = medals[index - 1] if index <= 3 else f"#{index:02d}"
            lines.append(f"{icon}  {name}  •  💰 {coins:,}")

    lines.extend([
        "",
        "━━━━━━━━━━━━━━━━━━━━",
        f"📊 Showing Top {len(rows)} only",
        "🔄 Coin balance အလိုက် အလိုအလျောက် Update ဖြစ်ပါတယ်။",
    ])

    await message.reply_text("\n".join(lines))

# =========================
# MAIN
# =========================

async def post_init(application: Application):
    await init_db()
    set_db_pool(db_pool)
    set_bu_gyi_db_pool(db_pool)
    set_tree_battle_db_pool(db_pool)


async def register_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user = query.from_user
        # Check whether user joined the private group
    try:
        member = await context.bot.get_chat_member(
            chat_id=GROUP_ID,
            user_id=user.id
        )

        is_member = (
            member.status in ("member", "administrator", "creator")
            or (
                member.status == "restricted"
                and getattr(member, "is_member", False)
            )
        )

    except Exception as e:
        logger.error("Group membership check failed: %s", e)

        keyboard = [
            [
                InlineKeyboardButton(
                    "🔗 Join Card Collection Group",
                    url=GROUP_INVITE_LINK
                )
            ],
            [
                InlineKeyboardButton(
                    "🔄 I Joined — Check Again",
                    callback_data="register"
                )
            ]
        ]

        await query.edit_message_text(
            "⚠️ Group membership ကို စစ်ဆေးလို့မရသေးပါ။\n\n"
            "Bot ကို Group ထဲထည့်ထားပြီး Admin ခွင့်ပြုချက် "
            "ပေးထားကြောင်း စစ်ဆေးပါ။",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    if not is_member:
        keyboard = [
            [
                InlineKeyboardButton(
                    "🔗 Join Card Collection Group",
                    url=GROUP_INVITE_LINK
                )
            ],
            [
                InlineKeyboardButton(
                    "✅ I Joined — Check Again",
                    callback_data="register"
                )
            ]
        ]

        await query.edit_message_text(
            "🔒 Register လုပ်ရန် Group ထဲကို အရင်ဝင်ပါ။\n\n"
            "၁။ အောက်က Join Group ကိုနှိပ်ပါ။\n"
            "၂။ Group ထဲဝင်ပြီးပါက Check Again ကိုနှိပ်ပါ။",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return
    async with db_pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT telegram_id FROM users WHERE telegram_id=$1",
            user.id
        )

        if row:
            await query.edit_message_text("✅ Already Registered")
            return

        await conn.execute(
            """
            INSERT INTO users
            (telegram_id, username, first_name, coins)
            VALUES ($1,$2,$3,100)
            """,
            user.id,
            user.username,
            user.first_name
        )

    await query.edit_message_text(
        f"🔮 မင်္ဂလာပါ {user.first_name}!\n\n"
        "🃏 MyCard Fortune Bot မှ ကြိုဆိုပါတယ်။\n\n"
        "💰 လက်ကျန် Coins: 100\n\n"
        "အသုံးပြုနိုင်သော Commands:\n"
        "/mycard - 🔮 Card Reading\n"
        "/game - 🎮 Daily Game\n"
        "/dailycoin - 💰 Daily Coin\n"
        "/mycoin - 💰 မိမိပိုင်ဆိုင်သော Coin\n"
        "/rank - 👑 Global Coin Top 10\n"
        "/help - 📖 Help"
    )

        # Notify group after successful registration
    try:
        async with db_pool.acquire() as conn:
            total_users = await conn.fetchval(
                "SELECT COUNT(*) FROM users"
            )

        username = (
            f"@{user.username}"
            if user.username
            else "မရှိပါ"
        )

        await context.bot.send_message(
            chat_id=GROUP_ID,
            text=(
                "🎉 New Member Registered!\n\n"
                f"👤 Name: {user.full_name}\n"
                f"🔗 Username: {username}\n"
                f"🆔 User ID: {user.id}\n"
                f"👥 Total Registered Users: {total_users}"
            )
        )

    except Exception as e:
        logger.error(
            "Registration group notification failed: %s",
            e
        )


async def bot_join_group(update, context):
    if update.my_chat_member:
        chat = update.my_chat_member.chat
        status = update.my_chat_member.new_chat_member.status

        if status in ["member", "administrator"]:
            keyboard = [
                [
                    InlineKeyboardButton(
                        "🔮 Tarot ကြည့်မယ်",
                        callback_data="group_tarot"
                    )
                ]
            ]

            await context.bot.send_message(
                chat_id=chat.id,
                text="🔮 Tarot Ready\n\n👇 ကဒ်ကြည့်ရန်နှိပ်ပါ",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
async def delete_message_after(context, chat_id, message_id, seconds):
    await asyncio.sleep(seconds)

    try:
        await context.bot.delete_message(
            chat_id=chat_id,
            message_id=message_id
        )
    except Exception:
        pass


async def expire_gift(context, chat_id, message_id, gift_id):
    await asyncio.sleep(60)

    async with db_pool.acquire() as conn:
        expired = await conn.fetchval(
            """
            UPDATE coin_gifts
            SET status = 'expired'
            WHERE id = $1 AND status = 'open'
            RETURNING id
            """,
            gift_id
        )

    if expired:
        try:
            await context.bot.delete_message(
                chat_id=chat_id,
                message_id=message_id
            )
        except Exception:
            pass

# =========================
# GROUP COIN GIFT SYSTEM
# =========================

async def gift_command(update, context):
    chat = update.effective_chat
    user = update.effective_user

    # Group ထဲမှာပဲ အသုံးပြုနိုင်သည်
    if chat.type not in ("group", "supergroup"):
        return await update.message.reply_text(
            "❌ ဒီ Command ကို Group ထဲမှာပဲ အသုံးပြုနိုင်ပါတယ်။"
        )

    if len(context.args) != 2:
        return await update.message.reply_text(
            "🎁 Coin မုန့်ဖိုးပေးရန်\n\n"
            "ဥပမာ: /g 200 5\n"
            "ပထမနံပါတ် = စုစုပေါင်း Coins\n"
            "ဒုတိယနံပါတ် = လက်ခံမည့်လူဦးရေ"
        )

    try:
        total = int(context.args[0])
        slots = int(context.args[1])
    except ValueError:
        return await update.message.reply_text(
            "❌ ဂဏန်းများသာ ထည့်ပါ။ ဥပမာ /g 200 5"
        )

    if total <= 0 or slots <= 0:
        return await update.message.reply_text(
            "❌ Coins နဲ့ လူဦးရေဟာ 0 ထက်ကြီးရပါမယ်။"
        )

    if total % slots != 0:
        return await update.message.reply_text(
            "❌ စုစုပေါင်း Coins ကို လူဦးရေနဲ့ အညီအမျှ ခွဲလို့ရတဲ့ ပမာဏထည့်ပါ။"
        )

    per_person = total // slots

    async with db_pool.acquire() as conn:
        async with conn.transaction():
            sender = await conn.fetchrow(
                """
                SELECT coins FROM users
                WHERE telegram_id = $1
                FOR UPDATE
                """,
                user.id,
            )

            if not sender:
                return await update.message.reply_text(
                    "❌ Register လုပ်ထားသူများသာ Coin ပေးနိုင်ပါတယ်။"
                )

            if sender["coins"] < total:
                return await update.message.reply_text(
                    f"❌ Coin မလုံလောက်ပါ။\n"
                    f"လက်ကျန်: {sender['coins']} Coins\n"
                    f"လိုအပ်ချက်: {total} Coins"
                )

            await conn.execute(
                """
                UPDATE users
                SET coins = coins - $1
                WHERE telegram_id = $2
                """,
                total,
                user.id,
            )

            gift_id = await conn.fetchval(
                """
                INSERT INTO coin_gifts
                (chat_id, creator_id, total_amount, slots, per_person)
                VALUES ($1, $2, $3, $4, $5)
                RETURNING id
                """,
                chat.id,
                user.id,
                total,
                slots,
                per_person,
            )

    try:
        message = await update.message.reply_text(
            f"🎁 COIN မုန့်ဖိုး\n\n"
            f"👤 ပေးသူ: {user.first_name}\n"
            f"💰 စုစုပေါင်း: {total} Coins\n"
            f"🎯 လက်ခံမည့်သူ: {slots} ယောက်\n"
            f"🪙 တစ်ယောက်လျှင်: {per_person} Coins\n\n"
            f"👇 Claim ခလုတ်ကို အရင်နှိပ်သူ {slots} ယောက် ရပါမယ်။",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(
                    f"🎁 Claim ({slots} ယောက်)",
                    callback_data=f"gift_claim:{gift_id}",
                )]
            ]),
        )

        async with db_pool.acquire() as conn:
            await conn.execute(
                """
                UPDATE coin_gifts
                SET message_id = $1
                WHERE id = $2
                """,
                message.message_id,
                gift_id,
            )

    except Exception:
        # Message မပို့နိုင်ပါက Coin ပြန်အမ်းပြီး Gift ကိုဖျက်ပါ
        async with db_pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute(
                    """
                    UPDATE users SET coins = coins + $1
                    WHERE telegram_id = $2
                    """,
                    total,
                    user.id,
                )
                await conn.execute(
                    "DELETE FROM coin_gifts WHERE id = $1",
                    gift_id,
                )
        raise


async def gift_claim_callback(update, context):
    query = update.callback_query
    user = query.from_user
    chat = query.message.chat

    if chat.type not in ("group", "supergroup"):
        return await query.answer(
            "Group ထဲမှာပဲ Claim လုပ်နိုင်ပါတယ်။",
            show_alert=True,
        )

    try:
        gift_id = int(query.data.split(":", 1)[1])
    except (ValueError, IndexError):
        return await query.answer(
            "❌ Gift အချက်အလက် မမှန်ပါ။",
            show_alert=True,
        )

    result = None

    async with db_pool.acquire() as conn:
        async with conn.transaction():
            gift = await conn.fetchrow(
                """
                SELECT * FROM coin_gifts
                WHERE id = $1 AND chat_id = $2
                FOR UPDATE
                """,
                gift_id,
                chat.id,
            )

            if not gift or gift["status"] != "open":
                result = ("closed", None)

            elif gift["creator_id"] == user.id:
                result = ("creator", None)

            elif gift["claimed_count"] >= gift["slots"]:
                result = ("closed", None)

            else:
                registered = await conn.fetchval(
                    """
                    SELECT 1 FROM users
                    WHERE telegram_id = $1
                    """,
                    user.id,
                )

                if not registered:
                    result = ("unregistered", None)
                else:
                    already_claimed = await conn.fetchval(
                        """
                        SELECT 1 FROM coin_gift_claims
                        WHERE gift_id = $1 AND user_id = $2
                        """,
                        gift_id,
                        user.id,
                    )

                    if already_claimed:
                        result = ("duplicate", None)
                    else:
                        await conn.execute(
                            """
                            INSERT INTO coin_gift_claims
                            (gift_id, user_id)
                            VALUES ($1, $2)
                            """,
                            gift_id,
                            user.id,
                        )

                        await conn.execute(
                            """
                            UPDATE users
                            SET coins = coins + $1
                            WHERE telegram_id = $2
                            """,
                            gift["per_person"],
                            user.id,
                        )

                        claimed = gift["claimed_count"] + 1
                        status = (
                            "claimed"
                            if claimed >= gift["slots"]
                            else "open"
                        )

                        await conn.execute(
                            """
                            UPDATE coin_gifts
                            SET claimed_count = $1, status = $2
                            WHERE id = $3
                            """,
                            claimed,
                            status,
                            gift_id,
                        )

                        result = (
                            "success",
                            (gift["per_person"], claimed, gift["slots"], status),
                        )

    if result[0] == "creator":
        return await query.answer(
            "❌ ကိုယ်ပေးထားတဲ့ Gift ကို ကိုယ်တိုင် Claim မလုပ်နိုင်ပါ။",
            show_alert=True,
        )

    if result[0] == "closed":
        return await query.answer(
            "❌ ဒီ Gift က Claim ပြည့်သွားပါပြီ။",
            show_alert=True,
        )

    if result[0] == "unregistered":
        return await query.answer(
            "❌ အရင်ဆုံး Bot မှာ Register လုပ်ပါ။",
            show_alert=True,
        )

    if result[0] == "duplicate":
        return await query.answer(
            "❌ ဒီ Gift ကို Claim လုပ်ပြီးပါပြီ။",
            show_alert=True,
        )

    amount, claimed, slots, status = result[1]

    await query.answer(f"🎉 +{amount} Coins ရရှိပါပြီ!")

    await query.message.reply_text(
        f"🎉 {user.first_name} က {amount} Coins ရရှိသွားပါပြီ။\n"
        f"👥 Claim: {claimed}/{slots}"
    )

    if status == "claimed":
        try:
            await query.message.edit_reply_markup(reply_markup=None)
        except Exception:
            pass


async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Owner-only broadcast to registered users and groups recorded by game activity."""
    user = update.effective_user
    message = update.effective_message
    if not user or user.id != OWNER_ID or not message:
        return

    source = message.reply_to_message
    broadcast_text = " ".join(context.args).strip()
    if source is None and not broadcast_text:
        await message.reply_text(
            "📣 Broadcast အသုံးပြုပုံ\n\n"
            "စာသားပို့ရန်: /broadcast မင်္ဂလာပါ\n"
            "ပုံ/ဖိုင်/စာသားပို့ရန် မူရင်း Message ကို Reply လုပ်ပြီး /broadcast ရိုက်ပါ။"
        )
        return

    status_message = await message.reply_text("📣 Broadcast စတင်နေပါပြီ…")
    async with db_pool.acquire() as conn:
        users = await conn.fetch("SELECT telegram_id FROM users ORDER BY telegram_id")
        groups = await conn.fetch(
            """SELECT group_id AS chat_id FROM group_tarot WHERE group_id < 0
               UNION SELECT chat_id FROM game_history WHERE chat_id < 0
               UNION SELECT chat_id FROM coin_gifts WHERE chat_id < 0
               ORDER BY chat_id"""
        )

    user_ok = user_fail = group_ok = group_fail = 0
    for row in users:
        target_id = int(row["telegram_id"])
        try:
            if source:
                await context.bot.copy_message(
                    chat_id=target_id, from_chat_id=source.chat_id,
                    message_id=source.message_id
                )
            else:
                await context.bot.send_message(chat_id=target_id, text=broadcast_text)
            user_ok += 1
        except Exception as exc:
            user_fail += 1
            logger.info("Broadcast to user %s failed: %s", target_id, exc)
        await asyncio.sleep(0.04)

    for row in groups:
        chat_id = int(row["chat_id"])
        try:
            if source:
                await context.bot.copy_message(
                    chat_id=chat_id, from_chat_id=source.chat_id,
                    message_id=source.message_id
                )
            else:
                await context.bot.send_message(chat_id=chat_id, text=broadcast_text)
            group_ok += 1
        except Exception as exc:
            group_fail += 1
            logger.info("Broadcast to group %s failed: %s", chat_id, exc)
        await asyncio.sleep(0.08)

    await status_message.edit_text(
        "✅ Broadcast ပြီးပါပြီ။\n\n"
        f"👤 မှတ်ပုံတင်ထားသော User: {len(users):,} ဦး\n"
        f"✅ ပို့အောင်မြင်: {user_ok:,} ဦး\n"
        f"⚠️ မပို့နိုင်: {user_fail:,} ဦး\n\n"
        f"👥 မှတ်တမ်းရှိ Group: {len(groups):,} ခု\n"
        f"✅ Group ပို့အောင်မြင်: {group_ok:,} ခု\n"
        f"⚠️ Group မပို့နိုင်: {group_fail:,} ခု"
    )

def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN is not set!")

    if not DATABASE_URL:
        raise ValueError("DATABASE_URL is not set!")

    app = (
        Application.builder()
        .token(BOT_TOKEN)
        .concurrent_updates(32)
        .post_init(post_init)
        .build()
    )

    app.add_handler(
        ChatMemberHandler(
            bot_join_group,
            ChatMemberHandler.MY_CHAT_MEMBER
        )
    )


    app.add_handler(
        MessageHandler(filters.ALL & ~filters.COMMAND, track_group_member),
        group=-1,
    )


    app.add_handler(CommandHandler("all", all_command))
    app.add_handler(CommandHandler("stop", stop_all_command))

    app.add_handler(
        CommandHandler("start", start)
    )
    app.add_handler(CommandHandler("broadcast", broadcast_command))

    # Tree Cutting 1Vs1 Battle (separate module; existing games unchanged)
    app.add_handler(CommandHandler("treebattle", treebattle_command))
    app.add_handler(CommandHandler("treecancel", treebattle_cancel_command))
    app.add_handler(CallbackQueryHandler(treebattle_callback, pattern=r"^tree:(join|chop):-?\d+$"))

    app.add_handler(
        CommandHandler("help", help_command)
    )

    app.add_handler(
        CommandHandler("rank", rank_command)
    )

    app.add_handler(
        CommandHandler("mycard", mycard_command)
    )

    app.add_handler(
      CommandHandler("game", game_command)
    )

    app.add_handler(
        CommandHandler("dailycoin", dailycoin_command)
    )

    app.add_handler(
        CommandHandler("mycoin", mycoin_command)
    )

    app.add_handler(
        CommandHandler("give", give_command)
    )

    app.add_handler(
        CommandHandler("addcoin", addcoin_command)
    )

    app.add_handler(CommandHandler("takecoin", takecoin_command))
    app.add_handler(CommandHandler("takeallcoins", takeallcoins_command))
    app.add_handler(
    CommandHandler("allcoin", allcoin_command)
   )

    app.add_handler(
    CallbackQueryHandler(tarot_callback, pattern="^card_")
)

    app.add_handler(
        CommandHandler("coin", coin_command)
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            group_tarot_counter
        )
    )


    print("🤖 MyCard Bot is running...")


    app.add_handler(
        CallbackQueryHandler(register_callback, pattern="^register$")
    )

    app.add_handler(
        CallbackQueryHandler(
            group_tarot_callback,
            pattern="^group_tarot$"
        )
    )

    app.add_handler(
    CallbackQueryHandler(
        game_callback,
        pattern=r"^game_bet:(10|100|1000|5000|10000)$"
    )
)
    app.add_handler(
    CommandHandler("g", gift_command)
)

    app.add_handler(
    CallbackQueryHandler(
        gift_claim_callback,
        pattern=r"^gift_claim:\d+$"
    )
)
    app.add_handler(
        CommandHandler("mafia", mafia_command)
    )

    app.add_handler(
        CallbackQueryHandler(
            mafia_callback,
            pattern=r"^mafia:"
        )
    )
    app.add_handler(
    CommandHandler("mafiastop", mafia_stop_command)
)

    # =========================
    # MYANMAR BU GYI GAME
    # =========================

    app.add_handler(
        CommandHandler("bugyi", bu_gyi_command)
    )

    app.add_handler(
        CommandHandler("bugyi_join", bu_gyi_join_command)
    )

    app.add_handler(
        CommandHandler("bugyi_bet", bu_gyi_bet_command)
    )

    app.add_handler(
        CommandHandler("bugyi_deal", bu_gyi_deal_command)
    )

    app.add_handler(
        CallbackQueryHandler(
            bu_gyi_callback,
            pattern=r"^bugyi:"
        )
    )
    app.run_polling()

if __name__ == "__main__":
    main()
