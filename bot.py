import telebot
import json
import os

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

ADMIN_ID = 7206565404
SUPPORT = "@Toji_fusiiguru"

USERS_FILE = "users.json"

# ---------------- USERS ----------------

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}

    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

# ---------------- MENU ----------------

def menu():
    markup = telebot.types.InlineKeyboardMarkup()

    markup.add(
        telebot.types.InlineKeyboardButton("👤 Profile", callback_data="profile"),
        telebot.types.InlineKeyboardButton("💎 Balance", callback_data="balance")
    )

    markup.add(
        telebot.types.InlineKeyboardButton("💳 Buy Points", callback_data="buy")
    )

    markup.add(
        telebot.types.InlineKeyboardButton("🎁 Invite & Earn", callback_data="refer")
    )

    markup.add(
        telebot.types.InlineKeyboardButton("👥 Telegram Members", callback_data="members")
    )

    markup.add(
        telebot.types.InlineKeyboardButton("👁 Telegram Views", callback_data="views")
    )

    markup.add(
        telebot.types.InlineKeyboardButton("❤️ Positive Reactions", callback_data="positive")
    )

    markup.add(
        telebot.types.InlineKeyboardButton("😡 Negative Reactions", callback_data="negative")
    )

    markup.add(
        telebot.types.InlineKeyboardButton("🔍 Track Order", callback_data="track")
    )

    markup.add(
        telebot.types.InlineKeyboardButton("📞 Support", callback_data="support")
    )

    return markup

# ---------------- START ----------------

@bot.message_handler(commands=["start"])
def start(message):
    users = load_users()
    uid = str(message.from_user.id)

    if uid not in users:
        users[uid] = {
            "username": message.from_user.username,
            "points": 0,
            "referrals": 0
        }

    save_users(users)

    bot.send_message(
        message.chat.id,
        "🚀 Welcome To Henry Boost Hub",
        reply_markup=menu()
    )

# ---------------- BUTTONS ----------------

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    users = load_users()
    uid = str(call.from_user.id)

    if uid not in users:
        return

    if call.data == "profile":
        u = users[uid]

        bot.send_message(
            call.message.chat.id,
            f"👤 Profile\n\n"
            f"🆔 ID: {uid}\n"
            f"👤 Username: @{u['username']}\n"
            f"💎 Points: {u['points']}\n"
            f"🎁 Referrals: {u['referrals']}"
        )

    elif call.data == "balance":
        bot.send_message(
            call.message.chat.id,
            f"💎 Balance: {users[uid]['points']} Points"
        )

    elif call.data == "buy":
        bot.send_message(
            call.message.chat.id,
            f"💳 Buy Points\n\n📞 Contact: {SUPPORT}"
        )

    elif call.data == "refer":
        bot.send_message(
            call.message.chat.id,
            f"🎁 Referral Link:\nhttps://t.me/{bot.get_me().username}?start={uid}"
        )

    elif call.data == "members":
        bot.send_message(
            call.message.chat.id,
            "👥 Telegram Members Service"
        )

    elif call.data == "views":
        bot.send_message(
            call.message.chat.id,
            "👁 Telegram Views Service"
        )

    elif call.data == "positive":
        bot.send_message(
            call.message.chat.id,
            "❤️ Positive Reactions Service"
        )

    elif call.data == "negative":
        bot.send_message(
            call.message.chat.id,
            "😡 Negative Reactions Service"
        )

    elif call.data == "track":
        bot.send_message(
            call.message.chat.id,
            "🔍 Send Your Order ID"
        )

    elif call.data == "support":
        bot.send_message(
            call.message.chat.id,
            f"📞 Support: {SUPPORT}"
        )

# ---------------- ADMIN ----------------

@bot.message_handler(commands=["addpoints"])
def addpoints(message):

    if message.from_user.id != ADMIN_ID:
        return

    try:
        _, uid, amount = message.text.split()

        users = load_users()

        if uid in users:
            users[uid]["points"] += int(amount)

            save_users(users)

            bot.send_message(
                int(uid),
                f"🎉 {amount} Points Added"
            )

            bot.reply_to(message, "✅ Done")

    except:
        bot.reply_to(
            message,
            "/addpoints user_id amount"
        )

# ---------------- STATS ----------------

@bot.message_handler(commands=["stats"])
def stats(message):

    if message.from_user.id != ADMIN_ID:
        return

    users = load_users()

    bot.reply_to(
        message,
        f"👥 Total Users: {len(users)}"
    )

# ---------------- RUN ----------------

print("BOT RUNNING...")
bot.infinity_polling()
