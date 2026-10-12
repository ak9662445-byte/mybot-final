import asyncio

import random

tarot_readings = {
"The Hierophant 📖": [
"✨ အလုပ်အကိုင်ပိုင်းတွင် စည်းကမ်းနဲ့ ကြိုးစားမှုကြောင့် အောင်မြင်မှုရလာနိုင်ပါတယ်။ အတွေ့အကြုံရှိသူထံမှ အကြံဉာဏ်ကောင်း ရရှိနိုင်ပါတယ်။",
"💰 ငွေကြေးပိုင်းမှာ တဖြည်းဖြည်းတိုးတက်လာမယ့် အခြေအနေရှိပါတယ်။ အလျင်စလို ဆုံးဖြတ်ခြင်းကို ရှောင်ပါ။",
"❤️ အချစ်ရေးမှာ ယုံကြည်မှုနဲ့ နားလည်မှုက အရေးကြီးပါတယ်။ ခိုင်မာတဲ့ဆက်ဆံရေး ဖြစ်လာနိုင်ပါတယ်။",
"🌙 စိတ်ထဲက ရည်မှန်းချက်တွေကို အကောင်အထည်ဖော်ဖို့ အချိန်ကောင်းဖြစ်ပါတယ်။",
"🔥 သတိထားရမယ့်အချက်က တခြားသူတွေရဲ့ စကားကို မစဉ်းစားဘဲ လိုက်လုပ်ခြင်း ဖြစ်ပါတယ်။",
"🌟 မမျှော်လင့်ထားတဲ့ အခွင့်အရေးအသစ်တစ်ခု ရောက်လာနိုင်ပါတယ်။",
"🎯 ကိုယ့်ရည်မှန်းချက်ကို မလွှတ်ဘဲ ဆက်လက်ကြိုးစားပါ။",
"🍀 ကံကောင်းခြင်းက တဖြည်းဖြည်းနဲ့ ဝင်လာမယ့်ပုံစံ ဖြစ်ပါတယ်။",
"🔮 အနာဂတ်မှာ အတွေ့အကြုံနဲ့ အသိပညာက အဓိကအင်အား ဖြစ်လာပါမယ်။",
"💎 အကြံပြုချက် - စိတ်ရှည်ပြီး မှန်ကန်တဲ့လမ်းကို ဆက်လျှောက်ပါ။"
]
}

import os

OWNER_ID = 8346244362
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
)

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

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
        min_size=1,
        max_size=5,
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

    logger.info("Database initialized successfully.")


# =========================
# START
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    async with db_pool.acquire() as conn:
        existing_user = await conn.fetchrow(
            """
            SELECT telegram_id, coins
            FROM users
            WHERE telegram_id = $1
            """,
            user.id,
        )

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"🔮 မင်္ဂလာပါ {user.first_name}!\n\n"
        "🎉 MyCard Fortune Bot 🌟\n\n"
        f"💰 Coins: {existing_user['coins']}",
        reply_markup=reply_markup
    )
    query = update.callback_query

    await query.answer()

    user = query.from_user

    async with db_pool.acquire() as conn:
        existing_user = await conn.fetchrow(
            """
            SELECT telegram_id, coins
            FROM users
            WHERE telegram_id = $1
            """,
            user.id,
        )

        if existing_user:
            await query.edit_message_text(
            '✅ Register ပြီးပါပြီ\n\n'
            '🎉 MyCard Fortune Bot 🌟\n\n'
            f'💰 Coins: {existing_user["coins"]}'
            )
            return

    await conn.execute("""
INSERT INTO users(
    telegram_id,
    username,
    first_name
)
VALUES($1,$2,$3)
ON CONFLICT DO NOTHING
""",
user.id,
user.username,
user.first_name
)


# =========================
# HELP
# =========================



async def tarot_callback(update, context):
    query = update.callback_query
    await query.answer(cache_time=1)

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
        await query.edit_message_text(
        await query.edit_message_text(
            "❌ Coin မလုံလောက်ပါ\n\n💰 လိုအပ်သော Coin: " + str(cost)
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
    ("The Fool 🃏", "https://upload.wikimedia.org/wikipedia/commons/9/90/RWS_Tarot_00_Fool.jpg"),
    ("The Magician 🪄", "https://upload.wikimedia.org/wikipedia/commons/d/de/RWS_Tarot_01_Magician.jpg"),
    ("The High Priestess 🌙", "https://upload.wikimedia.org/wikipedia/commons/8/88/RWS_Tarot_02_High_Priestess.jpg"),
    ("The Empress 👑", "https://upload.wikimedia.org/wikipedia/commons/d/d2/RWS_Tarot_03_Empress.jpg"),
    ("The Emperor 🏰", "https://upload.wikimedia.org/wikipedia/commons/c/c3/RWS_Tarot_04_Emperor.jpg"),
    ("The Hierophant 📖", "https://upload.wikimedia.org/wikipedia/commons/8/8d/RWS_Tarot_05_Hierophant.jpg"),
    ("The Lovers ❤️", "https://upload.wikimedia.org/wikipedia/commons/3/3a/RWS_Tarot_06_Lovers.jpg"),
    ("The Chariot 🛡️", "https://upload.wikimedia.org/wikipedia/commons/9/9b/RWS_Tarot_07_Chariot.jpg"),
    ("Strength 🦁", "https://upload.wikimedia.org/wikipedia/commons/f/f5/RWS_Tarot_08_Strength.jpg"),
    ("The Hermit 🕯️", "https://upload.wikimedia.org/wikipedia/commons/4/4d/RWS_Tarot_09_Hermit.jpg"),
    ("Wheel of Fortune 🎡", "https://upload.wikimedia.org/wikipedia/commons/3/3c/RWS_Tarot_10_Wheel_of_Fortune.jpg"),
    ("Justice ⚖️", "https://upload.wikimedia.org/wikipedia/commons/e/e0/RWS_Tarot_11_Justice.jpg"),
    ("The Hanged Man 🙃", "https://upload.wikimedia.org/wikipedia/commons/a/a4/RWS_Tarot_12_Hanged_Man.jpg"),
    ("Death 💀", "https://upload.wikimedia.org/wikipedia/commons/d/d7/RWS_Tarot_13_Death.jpg"),
    ("Temperance 🕊️", "https://upload.wikimedia.org/wikipedia/commons/f/f8/RWS_Tarot_14_Temperance.jpg"),
    ("The Devil 😈", "https://upload.wikimedia.org/wikipedia/commons/5/55/RWS_Tarot_15_Devil.jpg"),
    ("The Tower ⚡", "https://upload.wikimedia.org/wikipedia/commons/5/53/RWS_Tarot_16_Tower.jpg"),
    ("The Star ⭐", "https://upload.wikimedia.org/wikipedia/commons/d/db/RWS_Tarot_17_Star.jpg"),
    ("The Moon 🌙", "https://upload.wikimedia.org/wikipedia/commons/7/7f/RWS_Tarot_18_Moon.jpg"),
    ("The Sun ☀️", "https://upload.wikimedia.org/wikipedia/commons/1/17/RWS_Tarot_19_Sun.jpg"),
    ("Judgement 🔔", "https://upload.wikimedia.org/wikipedia/commons/d/dd/RWS_Tarot_20_Judgement.jpg"),
    ("The World 🌍", "https://upload.wikimedia.org/wikipedia/commons/f/ff/RWS_Tarot_21_World.jpg")
]

    count = int(data.split("_")[1])

    result = random.sample(cards, count)

    for name, image in result:

        reading = "\n".join(
            random.sample(
                tarot_readings.get(
                    name,
                    ["✨ သင့်အတွက် အဓိပ္ပါယ်ရှိသောကဒ်ဖြစ်ပါတယ်"]
                ),
                min(10, len(tarot_readings.get(name, [])))
            )
        )
        text = f"🔮 {name}\
\
{reading}\
\
✨ Tarot Reading Result"

        await context.bot.send_photo(
            chat_id=query.from_user.id,
            photo=image,
            caption=text
        )





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
            "💰 My Coin Balance

"
            f"👤 User: {update.effective_user.first_name}

"
            f"🪙 Coins: {row['coins']}

"
            "🔮 Tarot Card ကြည့်နိုင်ပါသည်"
        )
    else:
        await update.message.reply_text(
            "❌ Register မလုပ်ရသေးပါ
/start နှိပ်ပါ"
        )


async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.message.reply_text(
        "📖 MyCard Fortune Bot Help

"
        "/start - Bot စတင်ရန်
"
        "/help - အသုံးပြုနည်း
"
        "/mycard - 🔮 Card Reading
"
        "/dailycoin - 💰 Daily Coin
/mycoin - 💰 Check Coin Balance
"
        "/game - 🎮 Daily Game"
    )


# =========================
# PLACEHOLDER COMMANDS
# =========================

async def mycard_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

keyboard = [
        [
            InlineKeyboardButton(
                "🔮 1 Card (100 Coins)",
                callback_data="card_1"
            )
        ],
        [
            InlineKeyboardButton(
                "🔮 3 Cards (250 Coins)",
                callback_data="card_3"
            )
        ],
        [
            InlineKeyboardButton(
                "🔮 5 Cards (400 Coins)",
                callback_data="card_5"
            )
        ]
    ]

    await update.message.reply_text(
        "🔮 MyCard Reading

"
        "ဘယ်နှစ်ကဒ် ကြည့်မလဲ?",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )



async def game_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.message.reply_text(
        "🎮 Daily Game

"
        "🚧 Game System ကို V7 မှာ ထည့်သွင်းပေးပါမယ်။"
    )


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
                    "⏳ ဒီနေ့ Daily Coin ယူပြီးပါပြီ
မနက်ဖြန် ပြန်လာပါ"
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
        f"💰 Daily Coin ရရှိပါပြီ!

"
        f"🎁 +{reward} Coins

"
        "မနက်ဖြန် ပြန်ယူနိုင်ပါတယ်"
    )


# =========================
# MAIN
# =========================

async def post_init(
    application: Application
):
    await init_db()


def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN is not set!")

    if not DATABASE_URL:
        raise ValueError("DATABASE_URL is not set!")

    app = (
        Application.builder()
        .token(BOT_TOKEN)
        .post_init(post_init)
        .build()
    )

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CommandHandler("help", help_command)
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
        CommandHandler("addcoin", addcoin_command)
    )

    app.add_handler(
    CallbackQueryHandler(tarot_callback, pattern="^card_")
)

    app.add_handler(
        CommandHandler("coin", coin_command)
    )


    print("🤖 MyCard Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()
"""