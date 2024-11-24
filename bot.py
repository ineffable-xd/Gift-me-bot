import os
import random
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram import Bot

# Get the bot token from Scalingo environment variable
TOKEN = os.getenv('TOKEN')
USER_ID = 1972239827  # Your Telegram user ID

# List of gift links to be sent
gift_links = [
    "https://example.com/gift1",
    "https://example.com/gift2",
    "https://example.com/gift3",
    "https://example.com/gift4",
    "https://example.com/gift5",
    "https://example.com/gift6",
    "https://example.com/gift7",
]

# Random text to send after 6 gifts
random_text = [
    "Here's a little surprise for you! 🎁",
    "You deserve something special today! 💫",
    "Hope this brightens your day! ✨",
    "Enjoy your gift! 🎉",
    "A small token of appreciation for you! 💖",
    "You're awesome! Here's a surprise! 💌",
]

# Track how many times the user has received gifts
user_gift_count = {}

# Setup logging to send logs to your Telegram ID
def send_log(message: str):
    bot = Bot(token=TOKEN)
    bot.send_message(chat_id=USER_ID, text=message)

# Setup logging to file and console
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_gift(update: Update, context: CallbackContext):
    user_id = update.message.chat_id

    # Initialize gift count if user is new
    if user_id not in user_gift_count:
        user_gift_count[user_id] = 0

    # Log gift sending activity
    logger.info(f"User {user_id} requested a gift.")

    # Check if the user has received 6 gifts already
    if user_gift_count[user_id] < 6:
        # Send a gift link
        gift_link = random.choice(gift_links)
        update.message.reply_text(gift_link)
        user_gift_count[user_id] += 1
        send_log(f"Gift sent to {user_id}: {gift_link}")
    else:
        # Send a random message from random_text after 6 gifts
        random_message = random.choice(random_text)
        update.message.reply_text(random_message)
        user_gift_count[user_id] = 0  # Reset the gift count after sending the random message
        send_log(f"Random message sent to {user_id}: {random_message}")

def main():
    # Ensure that the token is available
    if not TOKEN:
        raise ValueError("No token found! Please set the 'TOKEN' environment variable.")
    
    # Create the Updater object and attach the bot token
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register command handlers
    dispatcher.add_handler(CommandHandler("surprise", send_gift))
    dispatcher.add_handler(CommandHandler("giftme", send_gift))

    # Send a start log to your Telegram ID
    send_log("Bot started successfully!")

    # Start the Bot
    updater.start_polling()

    # Run the bot until you send a signal to stop (Ctrl+C)
    updater.idle()

if __name__ == '__main__':
    main()
