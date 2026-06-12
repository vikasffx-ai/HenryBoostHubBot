import telebot
import json
import os

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

ADMIN_ID = 7206565404
SUPPORT_USERNAME = "@Toji_fusiiguru"
REFERRAL_REWARD = 100

USERS_FILE = "users.json"
ORDERS_FILE = "orders.json"

# --------------- LOAD USERS ---------------
def load_users():
    if not os.path.exists(USERS_FILE):
        return {}

    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

# --------------- LOAD ORDERS ---------------

def load_orders():
    if not os.path.exists(ORDERS_FILE):
        return []

    with open(ORDERS_FILE, "r") as f:
        return json.load(f)

def save_orders(data):
    with open(ORDERS_FILE, "w") as f:
        json.dump(data, f, indent=4)
# --------------- MENU ---------------
def menu():
    markup = telebot.types.InlineKeyboardMarkup()

    markup.add(
        telebot.types.InlineKeyboardButton("👤 Profile", callback_data="profile"),
        telebot.types.InlineKeyboardButton("💎 Balance", callback_data="balance")
    )

    markup.add(
        telebot.types.InlineKeyboardButton("💰 Buy Points", callback_data="buy_points")
    )

    markup.add(
        telebot.types.InlineKeyboardButton("🎁 Invite & Earn", callback_data="refer")
    )

    markup.add(
        telebot.types.InlineKeyboardButton("📦 Services", callback_data="services")
    )

    markup.add(
        telebot.types.InlineKeyboardButton("🔍 Track Order", callback_data="track")
    )

    markup.add(
        telebot.types.InlineKeyboardButton("📊 Statistics", callback_data="stats")
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

args = message.text.split()

if uid not in users:

    users[uid] = {
        "username": message.from_user.username,
        "points": 0,
        "referrals": 0
    }

    if len(args) > 1:

        ref = args[1]

        if ref != uid and ref in users:

            users[ref]["points"] += REFERRAL_REWARD
            users[ref]["referrals"] += 1

    save_users(users)

bot.send_message(
    message.chat.id,
    "🚀 Welcome To Henry Boost Hub",
    reply_markup=menu()
)

# ---------------- PROFILE ----------------

@bot.callback_query_handler(func=lambda call: True)
def callback(call):

users = load_users()
uid = str(call.from_user.id)

if uid not in users:
    return

if call.data == "profile":

    user = users[uid]

    bot.send_message(
        call.message.chat.id,
        f"👤 Profile\n\n"
        f"🆔 ID: {uid}\n"
        f"👤 Username: @{user['username']}\n"
        f"💎 Points: {user['points']}\n"
        f"🎁 Referrals: {user['referrals']}"
    )

elif call.data == "balance":

    bot.send_message(
        call.message.chat.id,
        f"💎 Balance: {users[uid]['points']} Points"
    )
    elif call.data == "buy_points":

        bot.send_message(
            call.message.chat.id,
            "💰 POINT PRICE LIST\n\n"
            "₹25 = 7,500 Points\n"
            "₹50 = 15,000 Points\n"
            "₹100 = 30,000 Points\n"
            "₹200 = 60,000 Points\n"
            "₹350 = 105,000 Points\n"
            "₹500 = 150,000 Points\n"
            "₹1000 = 300,000 Points\n\n"
            "📞 Contact Admin:\n"
            "@Toji_fusiiguru"
        )

    elif call.data == "refer":

        bot.send_message(
            call.message.chat.id,
            f"🎁 Invite & Earn\n\n"
            f"Earn 100 Points per referral.\n\n"
            f"https://t.me/{bot.get_me().username}?start={uid}"
        )

    elif call.data == "support":

        bot.send_message(
            call.message.chat.id,
            "📞 Support: @Toji_fusiiguru"
        )

    elif call.data == "stats":

        bot.send_message(
            call.message.chat.id,
            f"📊 Total Users: {len(users)}"
)
        # ---------------- RUN BOT ----------------

print("Bot Running...")

bot.infinity_polling(skip_pending=True)
