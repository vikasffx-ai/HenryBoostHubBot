import telebot
import json
import os

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

ADMIN_ID = 7206565404

USERS_FILE = "users.json"

# ---------------- LOAD / SAVE ----------------
def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(data):
    with open(USERS_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ---------------- MAIN MENU ----------------
def menu():
    markup = telebot.types.InlineKeyboardMarkup()

    markup.add(
    telebot.types.InlineKeyboardButton("👤 Profile", callback_data="profile"),
    telebot.types.InlineKeyboardButton("💎 Balance", callback_data="balance")
)

    markup.add(
    telebot.types.InlineKeyboardButton("💳 Buy Points", callback_data="buypoints"),
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

# ---------------- START (REFERRAL FIX) ----------------
@bot.message_handler(commands=['start'])
def start(message):
    users = load_users()
    uid = str(message.from_user.id)

    # referral system
    args = message.text.split()
    if len(args) > 1:
        ref = args[1]

        if ref != uid:
            if ref in users:
                users[ref]["points"] += 10
                users[ref]["referrals"] += 1

    if uid not in users:
        users[uid] = {
            "username": message.from_user.username,
            "points": 0,
            "referrals": 0
        }

    save_users(users)

    bot.send_message(message.chat.id,
                     "🚀 Welcome to Henry Boost Hub!",
                     reply_markup=menu())

# ---------------- CALLBACK ----------------
@bot.callback_query_handler(func=lambda call: True)
def cb(call):
    users = load_users()
    uid = str(call.from_user.id)

    if uid not in users:
        return

    if call.data == "profile":
        u = users[uid]
        bot.send_message(call.message.chat.id,
            f"👤 Profile\n\nID: {uid}\nUser: @{u['username']}\n💰 Points: {u['points']}\n🎁 Referrals: {u['referrals']}"
        )

    elif call.data == "balance":
        bot.send_message(call.message.chat.id,
            f"💰 Balance: {users[uid]['points']} Points"
        )

    elif call.data == "members":
        bot.send_message(call.message.chat.id,
            "👥 Send Order:\n/members 100"
        )

    elif call.data == "views":
        bot.send_message(call.message.chat.id,
            "👁 Send Order:\n/views 1000"
        )

    elif call.data == "reactions":
        bot.send_message(call.message.chat.id,
            "❤️ Send Order:\n/reactions 500"
        )

    elif call.data == "refer":
        bot.send_message(call.message.chat.id,
            f"🎁 Referral Link:\nhttps://t.me/{bot.get_me().username}?start={uid}"
        )

elif call.data == "buypoints":
    bot.send_message(call.message.chat.id,
        "💰 Buy Points\n\n📞 Contact: @Toji_fusiiguru"
    )

elif call.data == "track":
    bot.send_message(call.message.chat.id,
        "🔍 Apna Order ID bheje."
    )

elif call.data == "positive":
    bot.send_message(call.message.chat.id,
        "❤️ Positive Reactions Service"
    )

elif call.data == "negative":
    bot.send_message(call.message.chat.id,
        "😡 Negative Reactions Service"
    )

elif call.data == "support":
    bot.send_message(call.message.chat.id,
        "📞 Support: @Toji_fusiiguru"
                    )

# ---------------- ORDER COMMANDS ----------------
@bot.message_handler(commands=['members', 'views', 'reactions'])
def orders(message):
    bot.reply_to(message,
        "📦 Order received!\nAdmin will process it soon."
    )

# ---------------- ADMIN ----------------
@bot.message_handler(commands=['addpoints'])
def addpoints(message):
    if message.from_user.id != ADMIN_ID:
        return

    try:
        _, uid, amt = message.text.split()
        users = load_users()

        if uid in users:
            users[uid]["points"] += int(amt)
            save_users(users)

            bot.send_message(uid, f"🎉 +{amt} Points Added!")
            bot.reply_to(message, "Done")
    except:
        bot.reply_to(message, "Usage: /addpoints user_id amount")

# ---------------- STATS ----------------
@bot.message_handler(commands=['stats'])
def stats(message):
    if message.from_user.id != ADMIN_ID:
        return

    users = load_users()

    bot.reply_to(message,
        f"📊 Stats\n\n👥 Users: {len(users)}"
    )

# ---------------- RUN ----------------
print("🚀 FINAL PRO BOT RUNNING...")
bot.infinity_polling()
