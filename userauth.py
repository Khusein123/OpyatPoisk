from telebot.types import Message
import secrets
import string
import json
import time

KEY_FILE = "keys.json"
ADMIN_ID = 5292727929  # ваш Telegram chat_id

def save_keys(keys):
    with open(KEY_FILE, "w") as f:
        json.dump(keys, f)

def load_keys():
    try:
        with open(KEY_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def register_handlers(bot):
    @bot.message_handler(commands=['genkey'])
    def handle_genkey(message: Message):
        if message.chat.id != ADMIN_ID:
            bot.reply_to(message, "У вас нет доступа к этой команде.")
            return

        args = message.text.split()
        if len(args) != 2 or args[1] not in ["7", "30", "365"]:
            bot.reply_to(message, "Используйте: /genkey 7 или /genkey 30 или /genkey 365")
            return

        days = int(args[1])
        expire_at = int(time.time()) + days * 86400

        key = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(20))

        keys = load_keys()
        keys[key] = {"expire": expire_at, "activated_by": None}
        save_keys(keys)

        bot.reply_to(message, f"✅ Ключ на {days} дней создан:\n`{key}`", parse_mode="Markdown")
