import telebot
import json
import os

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

ADMIN_ID = 7206565404

# ---------------- FILES ----------------
USERS_FILE = "users.json"
REF_FILE = "referrals.json"
BAN_FILE = "banned.json"

def load(file):
    if not os.path.exists(file):
        return {}
    with open(file, "r") as f:
        return json.load(f)

def save(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

# ---------------- BUTTON MENU ----------------
def main_menu():
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(
        telebot.types.InlineKeyboardButton("👤 Profile", callback_data="profile"),
        telebot.types.InlineKeyboardButton("💰 Balance", callback_data="balance")
    )
    markup.add(
        telebot.types.InlineKeyboardButton("🎁 Refer", callback_data="refer"),
        telebot.types.InlineKeyboardButton("📞 Support", callback_data="support")
    )
    return markup

# ---------------- START ----------------
@bot.message_handler(commands=['start'])
def start(message):
    users = load(USERS_FILE)
    uid = str(message.from_user.id)

    if uid not in users:
        users[uid] = {
            "username": message.from_user.username,
            "points": 0,
            "referrals": 0
        }
        save(USERS_FILE, users)

    bot.send_message(
        message.chat.id,
        "🚀 Welcome to Henry Boost Hub!\nSelect option below:",
        reply_markup=main_menu()
    )

# ---------------- CALLBACK HANDLER ----------------
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    users = load(USERS_FILE)
    uid = str(call.from_user.id)

    if call.data == "profile":
        u = users.get(uid, {})
        text = f"""👤 Profile

ID: {uid}
Username: @{u.get('username')}
Points: {u.get('points',0)}
Referrals: {u.get('referrals',0)}"""
        bot.send_message(call.message.chat.id, text)

    elif call.data == "balance":
        points = users.get(uid, {}).get("points", 0)
        bot.send_message(call.message.chat.id, f"💰 Balance: {points} Points")

    elif call.data == "refer":
        bot.send_message(
            call.message.chat.id,
            f"🎁 Your Referral Link:\nhttps://t.me/{bot.get_me().username}?start={uid}"
        )

    elif call.data == "support":
        bot.send_message(call.message.chat.id, "📞 Contact: @Toji_fusiiguru")

# ---------------- ADMIN: BROADCAST ----------------
@bot.message_handler(commands=['broadcast'])
def broadcast(message):
    if message.from_user.id != ADMIN_ID:
        return

    users = load(USERS_FILE)
    text = message.text.replace("/broadcast", "").strip()

    for uid in users:
        try:
            bot.send_message(uid, f"📢 Broadcast:\n\n{text}")
        except:
            pass

    bot.reply_to(message, "✅ Broadcast sent!")

# ---------------- ADMIN: STATS ----------------
@bot.message_handler(commands=['stats'])
def stats(message):
    if message.from_user.id != ADMIN_ID:
        return

    users = load(USERS_FILE)

    bot.reply_to(
        message,
        f"""📊 Stats

👥 Users: {len(users)}
"""
    )

# ---------------- ADMIN: ADD POINTS ----------------
@bot.message_handler(commands=['addpoints'])
def addpoints(message):
    if message.from_user.id != ADMIN_ID:
        return

    try:
        _, uid, amt = message.text.split()
        users = load(USERS_FILE)

        if uid in users:
            users[uid]["points"] += int(amt)
            save(USERS_FILE, users)

            bot.send_message(uid, f"🎉 +{amt} Points Added!")
            bot.reply_to(message, "Done!")
    except:
        bot.reply_to(message, "Usage: /addpoints user_id amount")

# ---------------- RUN BOT ----------------
print("🚀 Advanced Bot Running...")
bot.infinity_polling()
