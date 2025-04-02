
from telegram.ext import Updater, CommandHandler
import sqlite3
from datetime import datetime, timedelta

# Database setup
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER, timestamp TEXT)")
conn.commit()

def save_user(user_id):
    now = datetime.now().isoformat()
    cursor.execute("INSERT INTO users (user_id, timestamp) VALUES (?, ?)", (user_id, now))
    conn.commit()

def get_mau():
    month_ago = datetime.now() - timedelta(days=30)
    cursor.execute("SELECT DISTINCT user_id FROM users WHERE timestamp > ?", (month_ago.isoformat(),))
    users = cursor.fetchall()
    return len(users)

def start(update, context):
    user_id = update.message.from_user.id
    save_user(user_id)
    update.message.reply_text("Botga hush kelibsiz!")

def mau_command(update, context):
    count = get_mau()
    update.message.reply_text(f"Oxirgi 30 kunda faol foydalanuvchilar: {count}")

def main():
    updater = Updater("7211219123:AAHR31aG56zOkvmNxk5NYlMSnVsZ8Noj_ug", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("mau", mau_command))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
