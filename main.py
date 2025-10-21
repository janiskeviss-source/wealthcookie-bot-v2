import telebot
import random
import os
import sqlite3
import requests
from flask import Flask, request
import json

app = Flask(__name__)
bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'))

# Fortune database
fortunes = [
    "🚀 BUSINESS: 'AI Instagram Captions'\n💰 PRICE: €29 per 10 captions\n📝 PROMPT: 'Create 10 engaging Instagram captions for [niche] businesses'\n👥 CLIENT SCRIPT: 'Hi [Business], I'll create 10 converting captions for €29.'",
    "🚀 BUSINESS: 'ChatGPT Prompt Pack'\n💰 PRICE: €17 one-time\n📝 PROMPT: 'Bundle 50 best prompts for viral content and marketing'\n👥 CLIENT SCRIPT: 'Get 50 proven prompts for €17 that actually work.'",
    "🚀 BUSINESS: 'AI Headshot Service'\n💰 PRICE: €19 per photo\n📝 PROMPT: 'Transform casual photos into professional headshots'\n👥 CLIENT SCRIPT: 'Need professional headshots? I use AI to create studio-quality photos for €19.'"
]

# Simple database to track payments
def init_db():
    conn = sqlite3.connect('payments.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS payments
                 (payment_id TEXT PRIMARY KEY, 
                  telegram_id INTEGER,
                  customer_email TEXT,
                  paid INTEGER DEFAULT 0)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return "🤖 WealthCookie Bot is running!"

# Stripe webhook endpoint
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Get webhook data
        payload = request.get_data(as_text=True)
        data = json.loads(payload)
        
        # Check if payment succeeded
        if data.get('type') == 'checkout.session.completed':
            session = data['data']['object']
            payment_id = session['id']
            customer_email = session.get('customer_details', {}).get('email', '')
            
            # Find which user made this payment
            conn = sqlite3.connect('payments.db')
            c = conn.cursor()
            c.execute("SELECT telegram_id FROM payments WHERE payment_id=?", (payment_id,))
            result = c.fetchone()
            
            if result:
                telegram_id = result[0]
                fortune = random.choice(fortunes)
                
                # Send fortune automatically!
                bot.send_message(
                    telegram_id,
                    f"🎉 **PAYMENT CONFIRMED!** 🎉\n\n"
                    f"🔮 **YOUR FORTUNE:**\n{fortune}\n\n"
                    f"✨ **Now go execute immediately!**\n"
                    f"Need help? Just reply to this message!"
                )
                print(f"✅ Fortune sent to user {telegram_id}")
            
            conn.close()
        
        return 'OK', 200
        
    except Exception as e:
        print(f"Webhook error: {e}")
        return 'Error', 400

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.InlineKeyboardMarkup()
    
    btn_pay = telebot.types.InlineKeyboardButton(
        "🎰 Get Fortune (€1)", 
        url="https://buy.stripe.com/dRm7sM7S1h2q9igeKU3VC00"
    )
    
    btn_preview = telebot.types.InlineKeyboardButton("👀 See Example", callback_data="free_preview")
    
    markup.add(btn_pay)
    markup.add(btn_preview)
    
    # Save user to database
    conn = sqlite3.connect('payments.db')
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO payments (telegram_id) VALUES (?)", (message.chat.id,))
    conn.commit()
    conn.close()
    
    bot.send_message(message.chat.id, 
                    "**🥠 WealthCookie Bot**\n\n"
                    "*Your €1 ticket to financial freedom*\n\n"
                    "🔮 Pay €1 → Get complete business blueprint\n"
                    "🤖 **AUTO-DELIVERY** - Fortune arrives instantly!\n"
                    "💸 Ready-to-use prompts & scripts\n\n"
                    "*This car started with one €1 decision...*",
                    reply_markup=markup,
                    parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data == "free_preview")
def free_preview(call):
    preview = "🚀 BUSINESS: 'AI Twitter Threads'\n💰 PRICE: €49 per thread\n📝 PROMPT: 'Create viral Twitter threads for tech accounts'"
    
    bot.send_message(call.message.chat.id,
                    f"👀 **EXAMPLE FORTUNE:**\n\n"
                    f"{preview}\n\n"
                    f"😉 *This could be YOURS with 1-click payment!*",
                    parse_mode='Markdown')

if __name__ == "__main__":
    print("🤖 WealthCookie Bot is running with AUTO-DELIVERY!")
    bot.polling()
