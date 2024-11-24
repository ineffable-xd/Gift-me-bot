import os
import random
import logging
from flask import Flask, request
import telebot

# Initialize Flask app
app = Flask(__name__)

# Get the bot token from Scalingo environment variable
TOKEN = os.getenv('TOKEN')
USER_ID = 1972239827  # Your Telegram user ID

# Initialize the bot
bot = telebot.TeleBot(TOKEN)

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
    bot.send_message(chat_id=USER_ID, text=message)

# Setup logging to file and console
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Command to send a gift or surprise
@bot.message_handler(commands=['surprise', 'giftme'])
def send_gift(message):
    user_id = message.chat.id

    # Initialize gift count if user is new
    if user_id not in user_gift_count:
        user_gift_count[user_id] = 0

    # Log gift sending activity
    logger.info(f"User {user_id} requested a gift.")

    # Check if the user has received 6 gifts already
    if user_gift_count[user_id] < 6:
        # Send a gift link
        gift_link = random.choice(gift_links)
        bot.reply_to(message, gift_link)
        user_gift_count[user_id] += 1
        send_log(f"Gift sent to {user_id}: {gift_link}")
    else:
        # Send a random message from random_text after 6 gifts
        random_message = random.choice(random_text)
        bot.reply_to(message, random_message)
        user_gift_count[user_id] = 0  # Reset the gift count after sending the random message
        send_log(f"Random message sent to {user_id}: {random_message}")

# Set up the webhook to trigger the bot when a message is received
@app.route('/webhook', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '!', 200

if __name__ == '__main__':
    # Set the webhook for Flask app
    bot.remove_webhook()
    bot.set_webhook(url='https://<your-app-name>.scalingo.app/webhook')

    # Start Flask app
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
