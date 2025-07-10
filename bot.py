import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

# Bot configuration with your token
TOKEN = '7625281149:AAHDBwnlo9wFzH8rT2A9zd8WsSU5DeM-FOk'
CHANNEL_USERNAME = "@yourchannel"  # Change to your actual channel
GROUP_USERNAME = "@yourgroup"      # Change to your actual group
TWITTER_USERNAME = "yourtwitter"   # Change to your actual Twitter

def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    welcome_message = (
        f"👋 Hello {user.first_name}!\n\n"
        "🚀 Welcome to our Airdrop Bot!\n\n"
        "To participate, please complete these steps:"
    )
    
    keyboard = [
        [InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")],
        [InlineKeyboardButton("👥 Join Group", url=f"https://t.me/{GROUP_USERNAME[1:]}")],
        [InlineKeyboardButton("🐦 Follow Twitter", url=f"https://twitter.com/{TWITTER_USERNAME}")],
        [InlineKeyboardButton("✅ Done All Steps", callback_data="completed_steps")]
    ]
    
    update.message.reply_text(
        welcome_message,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

def button_click(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    
    if query.data == "completed_steps":
        query.edit_message_text(
            "🎉 Great job completing the steps!\n\n"
            "Please send your *Solana wallet address* now to receive your 10 SOL reward!\n\n"
            "(Example: `HN5XQt7HgQJ7oyoj9QYcZEF7C6YFQbG1x8Xe3mJogVXY`)",
            parse_mode='Markdown'
        )

def handle_wallet(update: Update, context: CallbackContext) -> None:
    wallet_address = update.message.text.strip()
    
    # Basic Solana address validation
    if len(wallet_address) >= 32 and len(wallet_address) <= 44:
        update.message.reply_text(
            "✨ *Congratulations!* ✨\n\n"
            "Your 10 SOL reward is being processed!\n\n"
            "💰 Wallet: `{}`\n"
            "⏳ Expected within 24 hours\n\n"
            "Thank you for participating!".format(wallet_address),
            parse_mode='Markdown'
        )
    else:
        update.message.reply_text(
            "⚠️ Invalid Solana wallet address format.\n"
            "Please send a *valid* Solana wallet address (32-44 characters).\n\n"
            "Example: `HN5XQt7HgQJ7oyoj9QYcZEF7C6YFQbG1x8Xe3mJogVXY`",
            parse_mode='Markdown'
        )

def error(update: Update, context: CallbackContext) -> None:
    print(f"Error: {context.error}")

def main() -> None:
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button_click))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_wallet))
    dp.add_error_handler(error)

    print("🤖 Bot is running...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
