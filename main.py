import telebot
import random
import os
from flask import Flask

app = Flask(__name__)

# Get bot token from environment variable
bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'))

# Fortune database
fortunes = [
    "Offer 'AI Instagram Captions' for €29 - post on Fiverr today",
    "Flip expired domains with traffic - resell for 5x profit",
    "Create 'ChatGPT Prompt Pack' PDF - sell for €17 on Twitter",
    "Run 'AI Headshot' service - charge €19 per photo",
    "Resell Notion templates to students - €7 each on Reddit",
    "Cold DM 10 local businesses: 'I'll manage your social media for €499/month'",
    "Sell 'YouTube Title Pack' - 100 viral titles for €27",
    "Create 'AI Business Plan' service - charge €97 on Upwork",
    "Flip free AI tool credits - find trials, resell access for €15",
    "Offer 'TikTok Ghostwriting' - €50 per viral script"
]

@app.route('/')
def home():
    return "🤖 WealthCookie Bot is running!"

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.InlineKeyboardMarkup()
    
    btn_pay = telebot.types.InlineKeyboardButton("🎰 Get Fortune (€1)", callback_data="get_fortune")
    btn_preview = telebot.types.InlineKeyboardButton("👀 See Example", callback_data="free_preview")
    btn_subscribe = telebot.types.InlineKeyboardButton("📅 Daily Fortunes", callback_data="subscribe")
    
    markup.add(btn_pay)
    markup.add(btn_preview)
    markup.add(btn_subscribe)
    
    bot.send_message(message.chat.id, 
                    "**🥠 WealthCookie Bot**\n\n"
                    "*Your €1 ticket to financial freedom*\n\n"
                    "🔮 Pay €1 → Get proven money method\n"
                    "💸 Execute → Profit → Repeat\n"
                    "🚀 3,000+ fortunes delivered\n\n"
                    "*This car started with one €1 decision...*",
                    reply_markup=markup,
                    parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data == "get_fortune")
def send_fortune(call):
    fortune = random.choice(fortunes)
    
    markup = telebot.types.InlineKeyboardMarkup()
    btn_another = telebot.types.InlineKeyboardButton("🔄 Another Fortune", callback_data="get_fortune")
    btn_subscribe = telebot.types.InlineKeyboardButton("📅 Daily Fortunes", callback_data="subscribe")
    markup.add(btn_another, btn_subscribe)
    
    bot.send_message(call.message.chat.id,
                    f"🎉 **YOUR FORTUNE:**\n\n"
                    f"*{fortune}*\n\n"
                    f"✨ **Now go execute immediately.*\n"
                    f"📸 Screenshot your results and tag us!",
                    reply_markup=markup,
                    parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data == "free_preview")
def free_preview(call):
    preview = "Offer 'AI Twitter Threads' for €49 - businesses are begging for them"
    
    markup = telebot.types.InlineKeyboardMarkup()
    btn_get = telebot.types.InlineKeyboardButton("🚀 Get My Fortune", callback_data="get_fortune")
    markup.add(btn_get)
    
    bot.send_message(call.message.chat.id,
                    f"👀 **EXAMPLE FORTUNE:**\n\n"
                    f"*{preview}*\n\n"
                    f"😉 *This could have been YOUR fortune...*",
                    reply_markup=markup,
                    parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data == "subscribe")
def subscribe_info(call):
    bot.send_message(call.message.chat.id,
                    "**📅 Daily Fortune Subscription**\n\n"
                    "*€9/month = Fresh money method every morning*\n\n"
                    "Launching tomorrow - DM to get waitlisted!",
                    parse_mode='Markdown')

if __name__ == "__main__":
    print("🤖 WealthCookie Bot is running!")
    bot.polling()
