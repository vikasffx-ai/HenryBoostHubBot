import telebot
import json
import os
import config

TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)

# Load users
def load_users():
    with open("users.json", "r") as f:
        return json.load(f)

# Save users
def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f, indent=4)

# Start Command
@bot.message_handler(commands=['start'])
def start(message):
    users = load_users()
    user_id = str(message.from_user.id)

    if user_id not in users:
        users[user_id] = {
            "username": message.from_user.username,
            "points": 0,
            "referrals": 0
        }
        save_users(users)

    bot.reply_to(
        message,
        "🚀 Welcome to Henry Boost Hub!\n\n"
        "Commands:\n"
        "/profile - View Profile\n"
        "/balance - Check Points\n"
        "/help - Support"
    )

# Profile Command
@bot.message_handler(commands=['profile'])
def profile(message):
    users = load_users()
    user_id = str(message.from_user.id)

    if user_id not in users:
        bot.reply_to(message, "Please use /start first.")
        return

    user = users[user_id]

    text = f"""
👤 Profile

🆔 ID: {user_id}
📛 Username: @{user['username']}
💎 Points: {user['points']}
🎁 Referrals: {user['referrals']}
"""

    bot.reply_to(message, text)

# Balance Command
@bot.message_handler(commands=['balance'])
def balance(message):
    users = load_users()
    user_id = str(message.from_user.id)

    points = users.get(user_id, {}).get("points", 0)

    bot.reply_to(
        message,
        f"💎 Your Balance: {points} Points"
    )

# Help Command
@bot.message_handler(commands=['help'])
def help_cmd(message):
    bot.reply_to(
        message,
        f"📞 Support: {config.SUPPORT_USERNAME}"
    )

# Statistics (Admin Only)
@bot.message_handler(commands=['stats'])
def stats(message):
    if message.from_user.id != config.ADMIN_ID:
        return

    users = load_users()

    bot.reply_to(
        message,
        f"📊 Statistics\n\n👥 Total Users: {len(users)}"
    )

print("🚀 Henry Boost Hub Advanced Bot Started")

bot.infinity_polling()