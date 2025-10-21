import os
import telebot
from telebot import types
import random

BOT_TOKEN = os.getenv('BOT_TOKEN')
STRIPE_TOKEN = os.getenv('STRIPE_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# Payment tiers
TIERS = {
    "starter": {
        "price": 100,  # 1€
        "title": "🚀 Starter Pack - 1€",
        "description": "5 AI Business Prompts + Basic Templates\nPerfect for getting started!",
        "content": [
            "🎯 5 Premium AI Business Idea Prompts",
            "📝 Basic Marketing Template Pack", 
            "💡 Quick Start Guide",
            "⚡ Instant Digital Delivery"
        ]
    },
    "pro": {
        "price": 1200,  # 12€
        "title": "💼 Pro Toolkit - 12€", 
        "description": "25 AI Prompts + Complete Business Templates\nEverything you need to scale!",
        "content": [
            "🤖 25 Premium AI Business Prompts",
            "📊 Complete Business Plan Templates",
            "📱 Social Media Content Calendar", 
            "✉️ Email Marketing Sequences",
            "🎨 Brand Identity Guide"
        ]
    },
    "master": {
        "price": 2800,  # 28€
        "title": "👑 Master Bundle - 28€",
        "description": "VIP Package + 1-on-1 Strategy Call\nMaximum results guaranteed!",
        "content": [
            "🚀 ALL Pro Content PLUS:",
            "📞 15min 1-on-1 Strategy Call",
            "🛠️ Custom AI Model Training", 
            "🔄 Lifetime Updates",
            "🎁 Exclusive Bonuses"
        ]
    }
}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    
    btn1 = types.InlineKeyboardButton("🚀 Starter - 1€", callback_data="tier_starter")
    btn2 = types.InlineKeyboardButton("💼 Pro - 12€", callback_data="tier_pro") 
    btn3 = types.InlineKeyboardButton("👑 Master - 28€", callback_data="tier_master")
    
    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)
    
    bot.send_message(
        message.chat.id,
        "🤖 *AI Business Accelerator*\n\n"
        "Choose your success package:\n\n"
        "🚀 **Starter (1€)** - Get started fast\n"  
        "💼 **Pro (12€)** - Complete toolkit\n"
        "👑 **Master (28€)** - VIP experience\n\n"
        "Which tier fits your goals?",
        parse_mode='Markdown',
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data.startswith("tier_"):
        tier = call.data.split("_")[1]
        send_invoice(call.message, tier)

def send_invoice(message, tier):
    tier_data = TIERS[tier]
    
    bot.send_invoice(
        message.chat.id,
        title=tier_data["title"],
        description=tier_data["description"],
        provider_token=STRIPE_TOKEN,
        currency="eur",
        prices=[types.LabeledPrice(tier_data["title"], tier_data["price"])],
        start_parameter=f"{tier}_package",
        invoice_payload=f"{tier}_payload"
    )

@bot.pre_checkout_query_handler(func=lambda query: True)
def pre_checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@bot.message_handler(content_types=['successful_payment'])
def handle_payment(message):
    # Determine which tier was purchased
    tier = None
    for t in TIERS:
        if TIERS[t]["title"] in message.successful_payment.invoice_payload:
            tier = t
            break
    
    if tier:
        tier_data = TIERS[tier]
        
        # Send the content
        content_msg = f"🎉 *Thank for your purchase!*\n\n*Your {tier_data['title']} includes:*\n\n"
        for item in tier_data["content"]:
            content_msg += f"✅ {item}\n"
        
        content_msg += f"\n📧 *Delivery:* Check your email within 5 minutes\n"
        content_msg += f"🤝 *Support:* @BusinessSupport\n"
        content_msg += f"⭐ *Review:* Please rate your experience!"
        
        bot.send_message(message.chat.id, content_msg, parse_mode='Markdown')
        
        # Upsell for starter tier
        if tier == "starter":
            markup = types.InlineKeyboardMarkup()
            btn = types.InlineKeyboardButton("⚡ Upgrade to Pro - 11€", callback_data="tier_pro")
            markup.add(btn)
            
            bot.send_message(
                message.chat.id,
                "💡 *Special Offer:* Want the complete Pro toolkit?\n"
                "Upgrade now and get 25 AI prompts + full business templates!",
                parse_mode='Markdown',
                reply_markup=markup
            )

print("🤖 AI Business Accelerator Bot is LIVE!")
bot.infinity_polling()
