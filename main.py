import telebot
import random
import os
from flask import Flask

app = Flask(__name__)
bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'))

fortunes = [
    "🚀 BUSINESS: 'AI Instagram Captions'\n💰 PRICE: €29 per 10 captions\n📝 PROMPT: 'Create 10 engaging Instagram captions for [niche] businesses'\n👥 CLIENT SCRIPT: 'Hi [Business], I'll create 10 converting captions for €29.'",
    "🚀 BUSINESS: 'ChatGPT Prompt Pack'\n💰 PRICE: €17 one-time\n📝 PROMPT: 'Bundle 50 best prompts for viral content and marketing'\n👥 CLIENT SCRIPT: 'Get 50 proven prompts for €17 that actually work.'"
]

@app.route('/')
def home():
    return "🤖 WealthCookie Bot is running!"

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.InlineKeyboardMarkup()
    
    btn_pay = telebot.types.InlineKeyboardButton(
        "🎰 Get Fortune (€1)", 
        callback_data="request_payment"
    )
    
    btn_preview = telebot.types.InlineKeyboardButton("👀 See Example", callback_data="free_preview")
    
    markup.add(btn_pay)
    markup.add(btn_preview)
    
    bot.send_message(message.chat.id, 
                    "**🥠 WealthCookie Bot**\n\n"
                    "*Your €1 ticket to financial freedom*\n\n"
                    "🔮 Pay €1 → Get complete business blueprint\n"
                    "💸 Ready-to-use prompts & scripts\n\n"
                    "*This car started with one €1 decision...*",
                    reply_markup=markup,
                    parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data == "request_payment")
def request_payment(call):
    bot.send_message(call.message.chat.id,
                    "🎯 **Get Your Fortune for €1**\n\n"
                    "Click below to pay securely:\n"
                    "🔗 https://buy.stripe.com/dRm7sM7S1h2q9igeKU3VC00\n\n"
                    "⚡ **After payment, DM me your receipt!**\n"
                    "I'll send your fortune immediately! 🎉",
                    parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data == "free_preview")
def free_preview(call):
    preview = "🚀 BUSINESS: 'AI Twitter Threads'\n💰 PRICE: €49 per thread\n📝 PROMPT: 'Create viral Twitter threads for tech accounts'"
    
    bot.send_message(call.message.chat.id,
                    f"👀 **EXAMPLE FORTUNE:**\n\n"
                    f"{preview}\n\n"
                    f"😉 *Pay €1 to get YOUR fortune!*",
                    parse_mode='Markdown')

if __name__ == "__main__":
    print("🤖 WealthCookie Bot is running!")
    bot.polling()
