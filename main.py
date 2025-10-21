import telebot
import random
import os
from flask import Flask

app = Flask(__name__)

# Get bot token from environment variable
bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'))

# Fortune database - COMPLETE business ideas
fortunes = [
    "🚀 BUSINESS: 'AI Instagram Captions'\n💰 PRICE: €29 per 10 captions\n📝 PROMPT: 'Create 10 engaging Instagram captions for [niche] businesses with hooks, stories, and CTAs'\n👥 CLIENT SCRIPT: 'Hi [Business], I'll create 10 converting captions for €29. Pay only if you love them.'\n📍 SELL ON: Fiverr, Twitter DMs, local Facebook groups",

    "🚀 BUSINESS: 'ChatGPT Prompt Pack'\n💰 PRICE: €17 one-time\n📝 PROMPT: 'Bundle 50 best prompts for viral content, business plans, and marketing copy'\n👥 CLIENT SCRIPT: 'Stop struggling with AI. Get 50 proven prompts for €17 that actually work.'\n📍 SELL ON: Twitter, Reddit r/ChatGPT, indie makers",

    "🚀 BUSINESS: 'AI Headshot Service'\n💰 PRICE: €19 per photo\n📝 PROMPT: 'Transform casual photos into professional headshots using AI styling'\n👥 CLIENT SCRIPT: 'Need professional headshots? I use AI to create studio-quality photos for €19.'\n📍 SELL ON: LinkedIn, freelance platforms, student groups",

    "🚀 BUSINESS: 'Notion Template Shop'\n💰 PRICE: €7-€27 per template\n📝 PROMPT: 'Create productivity templates for students, entrepreneurs, and content creators'\n👥 CLIENT SCRIPT: 'Organize your life/work with these AI-optimized Notion templates starting at €7.'\n📍 SELL ON: Notion template galleries, TikTok, Reddit",

    "🚀 BUSINESS: 'YouTube Title Pack'\n💰 PRICE: €27 for 100 titles\n📝 PROMPT: 'Generate 100 click-worthy YouTube titles for [niche] with proven engagement formulas'\n👥 CLIENT SCRIPT: 'Stop guessing what works. Get 100 viral-ready YouTube titles for €27.'\n📍 SELL ON: YouTube creator communities, Twitter"
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
    btn_subscribe = telebot.types.InlineKeyboardButton("📅 Daily Fortunes", callback_data="subscribe")
    
    markup.add(btn_pay)
    markup.add(btn_preview)
    markup.add(btn_subscribe)
    
    bot.send_message(message.chat.id, 
                    "**🥠 WealthCookie Bot**\n\n"
                    "*Your €1 ticket to financial freedom*\n\n"
                    "🔮 Pay €1 → Get complete business blueprint\n"
                    "💸 Ready-to-use prompts & scripts\n"
                    "🚀 Start making money today\n\n"
                    "*This car started with one €1 decision...*",
                    reply_markup=markup,
                    parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data == "request_payment")
def request_payment(call):
    bot.send_message(call.message.chat.id,
                    "🎯 **Get Your Fortune for €1**\n\n"
                    "Click below to pay securely:\n"
                    "🔗 https://buy.stripe.com/dRm7sM7S1h2q9igeKU3VC00\n\n"
                    "⚡ After payment, forward me the receipt for instant delivery!\n"
                    "💬 I'll DM your complete business blueprint immediately.",
                    parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data == "get_fortune")
def send_fortune(call):
    fortune = random.choice(fortunes)
    
    markup = telebot.types.InlineKeyboardMarkup()
    btn_another = telebot.types.InlineKeyboardButton("🔄 Another Fortune", callback_data="request_payment")
    btn_subscribe = telebot.types.InlineKeyboardButton("📅 Daily Fortunes", callback_data="subscribe")
    markup.add(btn_another, btn_subscribe)
    
    bot.send_message(call.message.chat.id,
                    f"🎉 **YOUR FORTUNE:**\n\n"
                    f"{fortune}\n\n"
                    f"✨ **Now go execute immediately!**\n"
                    f"📸 Show me your results!",
                    reply_markup=markup,
                    parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data == "free_preview")
def free_preview(call):
    preview = "🚀 BUSINESS: 'AI Twitter Threads'\n💰 PRICE: €49 per thread\n📝 PROMPT: 'Create engaging Twitter threads that go viral for tech and business accounts'\n👥 CLIENT SCRIPT: 'I write AI-optimized Twitter threads that get 100k+ views for €49.'\n📍 SELL ON: Twitter DMs to founders, tech companies"
    
    markup = telebot.types.InlineKeyboardMarkup()
    btn_get = telebot.types.InlineKeyboardButton("🚀 Get My Fortune", callback_data="request_payment")
    markup.add(btn_get)
    
    bot.send_message(call.message.chat.id,
                    f"👀 **EXAMPLE FORTUNE:**\n\n"
                    f"{preview}\n\n"
                    f"😉 *This could have been YOUR fortune...*",
                    reply_markup=markup,
                    parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data == "subscribe")
def subscribe_info(call):
    bot.send_message(call.message.chat.id,
                    "**📅 Daily Fortune Subscription**\n\n"
                    "*€9/month = Fresh business blueprint every morning*\n\n"
                    "✨ **What you get:**\n"
                    "• New proven business idea daily\n"
                    "• Exact prompts & scripts\n"
                    "• Pricing strategies\n"
                    "• Client acquisition methods\n\n"
                    "Launching next week - DM to get waitlisted!",
                    parse_mode='Markdown')

if __name__ == "__main__":
    print("🤖 WealthCookie Bot is running!")
    bot.polling()
