import telebot
import random
import os
import sqlite3
import stripe
from flask import Flask, request

app = Flask(__name__)

# Initialize
bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'))
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')  # You need this from Stripe dashboard

# Database setup
def init_db():
    conn = sqlite3.connect('fortunes.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS payments
                 (stripe_id TEXT, telegram_id INTEGER, fortune TEXT, paid INTEGER)''')
    conn.commit()
    conn.close()

init_db()

# Fortune database
fortunes = [
    "🚀 BUSINESS: 'AI Instagram Captions'\n💰 PRICE: €29 per 10 captions\n📝 PROMPT: 'Create 10 engaging Instagram captions for [niche] businesses with hooks, stories, and CTAs'\n👥 CLIENT SCRIPT: 'Hi [Business], I'll create 10 converting captions for €29. Pay only if you love them.'\n📍 SELL ON: Fiverr, Twitter DMs, local Facebook groups",
    "🚀 BUSINESS: 'ChatGPT Prompt Pack'\n💰 PRICE: €17 one-time\n📝 PROMPT: 'Bundle 50 best prompts for viral content, business plans, and marketing copy'\n👥 CLIENT SCRIPT: 'Stop struggling with AI. Get 50 proven prompts for €17 that actually work.'\n📍 SELL ON: Twitter, Reddit r/ChatGPT, indie makers"
]

@app.route('/')
def home():
    return "🤖 WealthCookie Bot is running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get('Stripe-Signature')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, os.environ.get('STRIPE_WEBHOOK_SECRET')
        )
    except ValueError:
        return 'Invalid payload', 400
    except stripe.error.SignatureVerificationError:
        return 'Invalid signature', 400

    # Handle successful payment
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        # Find user in database
        conn = sqlite3.connect('fortunes.db')
        c = conn.cursor()
        c.execute("SELECT telegram_id FROM payments WHERE stripe_id=?", (session['id'],))
        result = c.fetchone()
        
        if result:
            telegram_id = result[0]
            fortune = random.choice(fortunes)
            
            # Send fortune via DM
            bot.send_message(telegram_id,
                           f"🎉 **PAYMENT CONFIRMED!** 🎉\n\n"
                           f"🔮 **YOUR FORTUNE:**\n{fortune}\n\n"
                           f"✨ **Now go execute immediately!**")
            
            # Mark as delivered
            c.execute("UPDATE payments SET paid=1 WHERE stripe_id=?", (session['id'],))
            conn.commit()
        
        conn.close()

    return 'Success', 200

@bot.message_handler(commands=['start'])
def start(message):
    # Save user intent to database
    conn = sqlite3.connect('fortunes.db')
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO payments (telegram_id) VALUES (?)", (message.chat.id,))
    conn.commit()
    conn.close()
    
    markup = telebot.types.InlineKeyboardMarkup()
    btn_pay = telebot.types.InlineKeyboardButton("🎰 Get Fortune (€1)", callback_data="request_payment")
    btn_preview = telebot.types.InlineKeyboardButton("👀 See Example", callback_data="free_preview")
    markup.add(btn_pay, btn_preview)
    
    bot.send_message(message.chat.id, 
                    "**🥠 WealthCookie Bot**\n\n"
                    "*Your €1 ticket to financial freedom*\n\n"
                    "🔮 Pay €1 → Get complete business blueprint\n"
                    "🤖 **AUTO-DELIVERY** - Fortune arrives instantly after payment!\n"
                    "💸 Ready-to-use prompts & scripts\n\n"
                    "*This car started with one €1 decision...*",
                    reply_markup=markup,
                    parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data == "request_payment")
def request_payment(call):
    # Create Stripe checkout session
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'eur',
                    'product_data': {'name': 'WealthCookie Fortune'},
                    'unit_amount': 100,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='https://t.me/WealthCookie_Bot',
            cancel_url='https://t.me/WealthCookie_Bot',
        )
        
        # Save to database
        conn = sqlite3.connect('fortunes.db')
        c = conn.cursor()
        c.execute("UPDATE payments SET stripe_id=? WHERE telegram_id=?", (session.id, call.message.chat.id))
        conn.commit()
        conn.close()
        
        bot.send_message(call.message.chat.id,
                        f"🎯 **Get Your Fortune for €1**\n\n"
                        f"Click below to pay securely:\n"
                        f"🔗 {session.url}\n\n"
                        f"⚡ **Auto-delivery** - Your fortune arrives instantly after payment!",
                        parse_mode='Markdown')
                        
    except Exception as e:
        bot.send_message(call.message.chat.id, "⚠️ Payment system temporarily unavailable. Please try again later.")

# ... keep your existing free_preview and other functions ...

if __name__ == "__main__":
    print("🤖 WealthCookie Bot is running!")
    bot.polling()
