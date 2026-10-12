import random

from telegram import Update
from telegram.ext import ContextTypes
from game_cleanup import hide_command, reply_and_expire, schedule_delete

DB_POOL = None

MIN_BET = 1000
CARDS_PER_PLAYER = 5
COMMISSION_RATE = 0.10  # လောင်းကြေး၏ 10% ကို အနိုင်ရသည့်အခါ အကောက်ဖြတ်မည်

SUITS = ("♠", "♥", "♦", "♣")
RANKS = (
    ("A", 1),
    ("2", 2),
    ("3", 3),
    ("4", 4),
    ("5", 5),
    ("6", 6),
    ("7", 7),
    ("8", 8),
    ("9", 9),
    ("10", 10),
    ("J", 10),
    ("Q", 10),
    ("K", 10),
)


def set_db_pool(pool):
    """Use the existing database pool from bot.py."""
    global DB_POOL
    DB_POOL = pool


def _make_hand(deck):
    return [deck.pop() for _ in range(CARDS_PER_PLAYER)]


def _hand_text(cards):
    return "  ".join(f"{rank}{suit}" for rank, value, suit in cards)


def _score(cards):
    return sum(card[1] for card in cards)


async def _ensure_user(user, conn):
    await conn.execute(
        """
        INSERT INTO users
            (telegram_id, username, first_name, coins)
        VALUES ($1, $2, $3, 0)
        ON CONFLICT (telegram_id) DO UPDATE
        SET username = EXCLUDED.username,
            first_name = EXCLUDED.first_name
        """,
        user.id,
        user.username,
        user.first_name or user.full_name,
    )


async def bu_gyi_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    message = update.effective_message
    context.application.create_task(hide_command(context, message))

    if update.effective_chat.type == "private":
        await reply_and_expire(message, context, 
            "ဒီဂိမ်းကို Telegram Group ထဲမှာ ကစားပါ။"
        )
        return

    await reply_and_expire(message, context, 
        "🎴 MYANMAR BU GYI\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "🤖 ဒိုင် — Bot\n"
        "👥 ကစားသူ — ဘယ်သူမဆို ဝင်ကစားနိုင်သည်\n"
        f"💰 အနည်းဆုံးလောင်းကြေး — {MIN_BET:,} Coin\n"
        f"🃏 ဖဲ — တစ်ယောက်လျှင် {CARDS_PER_PLAYER} ချပ်\n"
        "🏆 အမှတ်ပေါင်း ပိုများသူနိုင်မည်\n"
        "🤝 အမှတ်တူလျှင် Bot နိုင်မည်\n"
        "💵 နိုင်လျှင် လောင်းကြေးအပါအဝင် 2 ဆမှ အကောက် 10% ဖြတ်ပြီး ပြန်ရမည်\n"
        "🧾 အကောက် — လောင်းကြေး၏ 10% (1000 = 100, 10000 = 1000)\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "ကစားရန် — /bugyi_bet 1000\n"
        "ဥပမာ — /bugyi_bet 5000"
    )


async def bu_gyi_bet_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    message = update.effective_message
    context.application.create_task(hide_command(context, message))
    user = update.effective_user

    if update.effective_chat.type == "private":
        await reply_and_expire(message, context, 
            "ဒီဂိမ်းကို Telegram Group ထဲမှာ ကစားပါ။"
        )
        return

    if DB_POOL is None:
        await reply_and_expire(message, context, 
            "⚠️ Database မချိတ်ဆက်ရသေးပါ။"
        )
        return

    if not context.args or not context.args[0].isdigit():
        await reply_and_expire(message, context, 
            f"အသုံးပြုပုံ — /bugyi_bet {MIN_BET}"
        )
        return

    amount = int(context.args[0])

    if amount < MIN_BET:
        await reply_and_expire(message, context, 
            f"အနည်းဆုံး {MIN_BET:,} Coin လောင်းရပါမယ်။"
        )
        return

    if amount > 1_000_000_000:
        await reply_and_expire(message, context, 
            "⚠️ လောင်းကြေးပမာဏ များလွန်းနေပါတယ်။"
        )
        return

    # Bot နှင့် ကစားသူအတွက် ဖဲ ၅ ချပ်စီ ဝေမည်။
    deck = [
        (rank, value, suit)
        for suit in SUITS
        for rank, value in RANKS
    ]
    random.shuffle(deck)

    bot_cards = _make_hand(deck)
    player_cards = _make_hand(deck)

    bot_score = _score(bot_cards)
    player_score = _score(player_cards)

    # အမှတ်ပိုများမှ ကစားသူနိုင်မည်။
    won = player_score > bot_score
    # အနိုင်ရလျှင် လောင်းကြေး၏ 10% ကို Bot အကောက်အဖြစ် ဖြတ်မည်။
    commission = int(amount * COMMISSION_RATE) if won else 0
    payout = amount * 2 - commission

    try:
        async with DB_POOL.acquire() as conn:
            async with conn.transaction():
                await _ensure_user(user, conn)

                # လောင်းကြေးကို အရင်နုတ်မည်။
                row = await conn.fetchrow(
                    """
                    UPDATE users
                    SET coins = coins - $1,
                        updated_at = NOW()
                    WHERE telegram_id = $2
                      AND coins >= $1
                    RETURNING coins
                    """,
                    amount,
                    user.id,
                )

                if row is None:
                    balance_row = await conn.fetchrow(
                        """
                        SELECT coins
                        FROM users
                        WHERE telegram_id = $1
                        """,
                        user.id,
                    )
                    balance = (
                        int(balance_row["coins"])
                        if balance_row
                        else 0
                    )

                    await reply_and_expire(message, context, 
                        "❌ Coin မလုံလောက်ပါ။\n"
                        f"💰 လက်ကျန် — {balance:,} Coin"
                    )
                    return

                # နိုင်လျှင် လောင်းကြေးအပါအဝင် 2 ဆ ပြန်ပေးမည်။
                if won:
                    await conn.execute(
                        """
                        UPDATE users
                        SET coins = coins + $1,
                            updated_at = NOW()
                        WHERE telegram_id = $2
                        """,
                        payout,
                        user.id,
                    )

                balance_row = await conn.fetchrow(
                    """
                    SELECT coins
                    FROM users
                    WHERE telegram_id = $1
                    """,
                    user.id,
                )
                balance = int(balance_row["coins"])

    except Exception:
        await reply_and_expire(message, context, 
            "⚠️ ဂိမ်းလုပ်ဆောင်ရာမှာ အမှားဖြစ်သွားပါတယ်။ "
            "ထပ်မကစားခင် /mycoin နဲ့ လက်ကျန်စစ်ပါ။"
        )
        raise

    if won:
        result = (
            f"🟢 သင်နိုင်ပါပြီ။ +{amount - commission:,} Coin အမြတ်\n"
            f"🧾 Bot အကောက် (10%) — {commission:,} Coin\n"
            f"💰 လောင်းကြေးအပါအဝင် ပြန်ရငွေ — "
            f"{payout:,} Coin"
        )
    else:
        result = (
            f"🔴 သင်ရှုံးပါပြီ။ -{amount:,} Coin\n"
            "🤖 ဒီတစ်ကြိမ်မှာ Bot က နိုင်ပါတယ်။\n"
            "🧾 ရှုံးသည့်အခါ လောင်းကြေးကိုသာ ဆုံးရှုံးပြီး အကောက်ထပ်မဖြတ်ပါ။"
        )

    name = user.full_name or user.first_name or "Player"

    result_message = await context.bot.send_message(
        chat_id=message.chat_id,
        text=(
            "🎴 MYANMAR BU GYI · ရလဒ်\n"
            "━━━━━━━━━━━━━━━━━━\n"
            f"👤 ကစားသူ — {name}\n"
            f"💰 လောင်းကြေး — {amount:,} Coin\n"
            "━━━━━━━━━━━━━━━━━━\n"
            f"🤖 Bot ဖဲ — {_hand_text(bot_cards)}\n"
            f"🔢 Bot အမှတ် — {bot_score}\n\n"
            f"👤 သင့်ဖဲ — {_hand_text(player_cards)}\n"
            f"🔢 သင့်အမှတ် — {player_score}\n"
            "━━━━━━━━━━━━━━━━━━\n"
            f"{result}\n"
            f"💳 လက်ကျန် — {balance:,} Coin\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "နောက်တစ်ကြိမ် ကစားရန် /bugyi_bet 1000"
        )
    )
    schedule_delete(context, result_message, 20)


# အဟောင်း bot.py ထဲက handler များနှင့်
# import error မဖြစ်စေရန် ထားထားသည်။
async def bu_gyi_join_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    message = update.effective_message
    context.application.create_task(hide_command(context, message))
    await reply_and_expire(message, context, 
        "Join လုပ်ရန် မလိုပါ။\n"
        "ကစားရန် /bugyi_bet 1000 ကို အသုံးပြုပါ။"
    )


async def bu_gyi_deal_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    message = update.effective_message
    context.application.create_task(hide_command(context, message))
    await reply_and_expire(message, context, 
        "ဒီဂိမ်းမှာ ဒိုင်က Bot ဖြစ်ပါတယ်။\n"
        "ကစားရန် /bugyi_bet 1000 ကို အသုံးပြုပါ။"
    )


async def bu_gyi_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query
    if query:
        await query.answer(
            "Join လုပ်ရန် မလိုပါ။ /bugyi_bet 1000 ကို သုံးပါ။",
            show_alert=True,
        )
