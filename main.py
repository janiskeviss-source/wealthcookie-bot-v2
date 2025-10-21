import os
import telebot
from telebot import types
import random

# Initialize bot
BOT_TOKEN = os.getenv('BOT_TOKEN')
STRIPE_TOKEN = os.getenv('STRIPE_TOKEN')  # Your Stripe provider token
bot = telebot.TeleBot(BOT_TOKEN)

# Fortune messages
FORTUNES = [
    "🎉 Great success is coming your way!",
    "💰 Financial abundance is near",
    "❤️ Love will surprise you soon", 
    "🚀 A big opportunity is approaching",
    "🌈 Your hard work will pay off",
    "🌟 Something wonderful will happen today",
    "🎯 Trust your instincts - they're right",
    "💫 Good news is on the way"
]

# /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    prices = [types.LabeledPrice("Fortune Cookie", 100)]  # 1€ = 100 cents
    
    bot.send_invoice(
        message.chat.id,
        title="🍪 Digital Fortune Cookie",
        description="Receive a personalized wealth fortune delivered via DM",
        provider_token=STRIPE_TOKEN,
        currency="eur",
        prices=prices,
        start_parameter="fortune-cookie",
        invoice_payload="fortune_cookie_payload"
    )

# Handle pre-checkout query (REQUIRED)
@bot.pre_checkout_query_handler(func=lambda query: True)
def pre_checkout(pre_checkout_query):
    try:
        bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
        print(f"✅ Pre-checkout approved for {pre_checkout_query.from_user.id}")
    except Exception as e:
        print(f"❌ Pre-checkout error: {e}")
        bot.answer_pre_checkout_query(pre_checkout_query.id, ok=False, error_message="Payment failed")

# Handle successful payment (THIS SENDS THE AUTOMATIC DM)
@bot.message_handler(content_types=['successful_payment'])
def handle_successful_payment(message):
    try:
        user_id = message.chat.id
        user_name = message.from_user.first_name
        
        # Get a random fortune
        fortune = random.choice(FORTUNES)
        
        # Send the automatic DM
        bot.send_message(
            user_id,
            f"🎊 *Congratulations {user_name}!*\n\n"
            f"**Your Fortune:** {fortune}\n\n"
            "Thank you for your purchase! ✨",
            parse_mode='Markdown'
        )
        
        print(f"✅ Fortune sent to user {user_id}: {fortune}")
        
    except Exception as e:
        print(f"❌ Error sending fortune: {e}")
        bot.send_message(
            message.chat.id,
            "❌ Sorry, there was an error delivering your fortune. Please contact support."
        )

# Handle regular messages
@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    if message.text and "fortune" in message.text.lower():
        # Send payment invoice for fortune requests
        prices = [types.LabeledPrice("Fortune Cookie", 100)]
        bot.send_invoice(
            message.chat.id,
            title="🍪 Digital Fortune Cookie",
            description="Receive a personalized wealth fortune",
            provider_token=STRIPE_TOKEN,
            currency="eur",
            prices=prices,
            start_parameter="fortune-cookie",
            invoice_payload="fortune_cookie_payload"
        )
    else:
        bot.send_message(
            message.chat.id,
            "Send /start to get your fortune cookie! 🍪"
        )

# Start the bot
print("🤖 WealthCookie Bot is running with AUTO-DELIVERY!")
bot.infinity_polling()
