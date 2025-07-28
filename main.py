import os
import telebot
import threading
import time
from flask import Flask
from keep_alive import keep_alive
from monitor import MonitorManager
import userauth
userauth.register_handlers(bot)
from menu import MenuBuilder
import os
TOKEN = "7905547591:AAEivoneinmUDRtg7hvBkGPEPPAegMC36uc"
CHAT_ID = "5292727929"
bot = telebot.TeleBot(TOKEN)

auth = UserAuth()
monitor = MonitorManager(bot, auth)
menu = MenuBuilder(bot)

@bot.message_handler(commands=['start'])
def start_cmd(message):
    menu.send_main_menu(message.chat.id)

@bot.message_handler(func=lambda m: m.text == "🔍 Поиски")
def start_search(m):
    monitor.command_monitor(m)

@bot.message_handler(func=lambda m: m.text == "📄 Инструкция")
def show_help(m):
    bot.send_message(m.chat.id, "Чтобы начать мониторинг, активируйте ключ в разделе 'Аккаунт'.")

@bot.message_handler(func=lambda m: m.text == "💼 Поддержка")
def support(m):
    bot.send_message(m.chat.id, "Напишите @Meneger_PoiskIphone по вопросам активации ключей.")

@bot.message_handler(func=lambda m: m.text == "👤 Аккаунт")
def account(m):
    user_id = str(m.from_user.id)
    if auth.is_key_active(user_id):
        bot.send_message(m.chat.id, "✅ Ключ активен.")
    else:
        bot.send_message(m.chat.id, "❌ Ключ не активирован. Введите: /activate КЛЮЧ")

@bot.message_handler(commands=['activate'])
def activate_key(m):
    parts = m.text.split()
    if len(parts) == 2:
        result = auth.activate_key(str(m.from_user.id), parts[1])
        bot.send_message(m.chat.id, result)
    else:
        bot.send_message(m.chat.id, "❗ Формат: /activate КЛЮЧ")

@bot.message_handler(commands=['genkey'])
def generate_key(m):
    if str(m.chat.id) == CHAT_ID:
        key = auth.generate_key()
        bot.send_message(m.chat.id, f"🔑 Новый ключ: {key}")
    else:
        bot.send_message(m.chat.id, "⛔ Только администратор может генерировать ключи.")

keep_alive()
threading.Thread(target=monitor.loop).start()
bot.polling(none_stop=True)
