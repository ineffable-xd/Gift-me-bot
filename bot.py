import telebot
import random
import logging
import os
import time

# Fetch the API token only once from environment variables
API_TOKEN = "7571171685:AAG-cbHDHzGq-bossU-lzG2uVLxLNc-YIRM"

# Check if the token is available
if not API_TOKEN:
    raise ValueError("API token is missing! Please set the 'API_TOKEN' environment variable.")

# Initialize the bot with the fetched API token
bot = telebot.TeleBot(API_TOKEN)

# Sample gifts and messages for the bot to send
gifts = ["https://example.com/gift1", "https://example.com/gift2", "https://example.com/gift1"]
random_messages = ["Here's a random message!", "Enjoy your day!", "Hope you're doing well!", "Stay awesome!"]

# Create a dictionary to track the number of gifts sent to each user
gift_sent_count = {}

# Function to handle the /giftme command
def handle_giftme(message):
    user_id = message.from_user.id

    if user_id not in gift_sent_count:
        gift_sent_count[user_id] = 0

    if gift_sent_count[user_id] < 6:
        gift = random.choice(gifts)
        bot.reply_to(message, gift)
        gift_sent_count[user_id] += 1
        logging.info(f"Gift sent to {user_id}. Total gifts sent: {gift_sent_count[user_id]}")
    else:
        random_message = random.choice(random_messages)
        bot.reply_to(message, random_message)
        logging.info(f"Sent random message to {user_id}")

# Set up a command handler for /giftme
@bot.message_handler(commands=['giftme'])
def giftme_command(message):
    handle_giftme(message)

# Start polling with error handling and logging
def start_polling():
    try:
        logging.info("Bot started...")
        bot.polling(none_stop=True)
    except Exception as e:
        logging.error(f"Error in bot polling: {e}")
        time.sleep(5)  # Delay before restarting polling
        start_polling()

# Run the bot in a loop
if __name__ == '__main__':
    start_polling()
