

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
from telegram.ext import MessageHandler, filters

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
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS group_tarot (
               group_id BIGINT PRIMARY KEY,
               count INTEGER DEFAULT 0,
               active BOOLEAN DEFAULT FALSE,
            last_user_id BIGINT,
            last_username TEXT
            );
        """)

    logger.info("Database initialized successfully.")


# =========================
# START
# =========================






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
        "🔮 Tarot Ready\n\n"
        "ဒီနေ့ သင့် ကံကြမာကို ရယူရန် နှိပ်ပါ👇",
        
        reply_markup=InlineKeyboardMarkup(keyboard)

    async def delete_ready():
        await asyncio.sleep(30)
        try:
            await ready_msg.delete()
        except:
            pass

    asyncio.create_task(delete_ready()
    
    )



async def group_tarot_callback(update, context):

    query = update.callback_query
    await query.answer()

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
                SET coins = coins + 10
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
        "🎁 Reward:\n+10 Coins"
    )


    photo = open(card_file,"rb")

    msg = await context.bot.send_photo(
        chat_id=chat_id,
        photo=photo,
        caption=caption
    )

    photo.close()


    await asyncio.sleep(10)


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
            "/dailycoin - 💰 Daily Coin\n"
            "/mycoin - 💰 မိမိပိုင်ဆိုင်သော Coin များ\n"
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
        coins = row["coins"] if row else 0

        await query.edit_message_text(
            "🔮 Tarot Reading မရသေးပါ ✨\n\n"
            "❌ Coin မလောက်သေးပါ\n\n"
            "💰 လိုအပ်သော Coin : " + str(cost) + "\n"
            "💎 လက်ရှိ Coin : " + str(coins) + "\n\n"
            "━━━━━━━━━━━━━━\n"
            "💳 Coin ဝယ်ယူရန် ဆက်သွယ်ပါ\n"
            "👑 Owner : @helixdemo\n\n"
            "🎮 Daily Game ကစားပြီး Coin ရယူနိုင်ပါတယ် ✨"
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

        await asyncio.sleep(2)

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
            await asyncio.sleep(1)

        await loading.edit_text(
            "🔥 Destiny Card Found!\n\n✨ Preparing your result..."
        )

        await asyncio.sleep(1)

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

    card_name = random.choice(list(tarot_cards.keys()))
    meaning = random.choice(tarot_cards[card_name])

    card_file = None
    for file in os.listdir('cards'):
        if card_name.lower().split()[1] in file.lower():
            card_file = 'cards/' + file
            break

    if not card_file:
        card_file = 'cards/00_Fool.jpg'

    image = open(card_file, "rb")

    await context.bot.send_photo(
        chat_id=query.message.chat.id,
        photo=image,
        caption=reading
    )

    image.close()


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
        "🔮 MyCard Reading"
        "ဘယ်နှစ်ကဒ် ကြည့်မလဲ?",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )



async def game_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.message.reply_text(
        "🎮 Daily Game"
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
# MAIN
# =========================

async def post_init(
    application: Application
):
    await init_db()




async def register_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user = query.from_user

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
        "/help - 📖 Help"
    )


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

    app.run_polling()


if __name__ == "__main__":
    main()