import os
import telebot
from telebot import types
import random

BOT_TOKEN = os.getenv('BOT_TOKEN')
STRIPE_TOKEN = os.getenv('STRIPE_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

FORTUNES = [
    "Great success is coming your way!",
    "Financial abundance is near",
    "A big opportunity is approaching"
]

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("🍪 Get Fortune - 1€", pay=True)
    markup.add(btn)
    bot.send_message(message.chat.id, "Click below:", reply_markup=markup)

@bot.pre_checkout_query_handler(func=lambda query: True)
def pre_checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@bot.message_handler(content_types=['successful_payment'])
def handle_payment(message):
    fortune = random.choice(FORTUNES)
    bot.send_message(message.chat.id, f"🎉 Your fortune: {fortune}")

print("Bot is running...")
bot.infinity_polling()
