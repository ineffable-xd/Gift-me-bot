import telebot
import random
import time
from datetime import datetime

# Telegram bot token and your Telegram ID
API_TOKEN = '7571171685:AAG-cbHDHzGq-bossU-lzG2uVLxLNc-YIRM'
MY_TELEGRAM_ID = '1972239827'

# Create the bot instance
bot = telebot.TeleBot(API_TOKEN)

# Define the gift list
GIFT_LIST = [
    'https://example.com/gift1', 'https://example.com/gift2', 
    'https://example.com/gift3', 'https://example.com/gift4', 
    'https://example.com/gift5', 'https://example.com/gift6'
]

# Define random messages to send after 6 gifts
RANDOM_MESSAGES_FILE = [
    "Hope you're enjoying the gifts!", 
    "Surprise! Here's a little something else for you.",
    "Keep the fun going with more surprises!",
    "Your gift awaits! Check it out!",
    "Here's another treat just for you!",
    "Enjoy your day with a bonus gift!"
]

# Initialize variables to keep track of usage
user_gift_counter = {}
last_reset_date = datetime.now().date()

# Function to check and reset the counter at midnight
def reset_counter_if_new_day():
    global last_reset_date
    current_date = datetime.now().date()
    if current_date != last_reset_date:
        last_reset_date = current_date
        user_gift_counter.clear()  # Reset all user counters

# Command to send gifts and surprise
@bot.message_handler(commands=['gift_me', 'surprise'])
def send_gift(message):
    reset_counter_if_new_day()  # Reset counter if it's a new day
    user_id = message.from_user.id
    user_gift_counter[user_id] = user_gift_counter.get(user_id, 0) + 1

    if user_gift_counter[user_id] <= 6:
        # Send a gift from the list
        gift = random.choice(GIFT_LIST)
        bot.send_message(user_id, f"Here is your gift: {gift}")
    else:
        # Send a random message after 6 gifts
        random_message = random.choice(RANDOM_MESSAGES_FILE)
        bot.send_message(user_id, random_message)

    # Send log to your Telegram ID
    log_message = f"User {user_id} requested a gift. Sent: {user_gift_counter[user_id] <= 6 and 'gift' or 'random message'}."
    bot.send_message(MY_TELEGRAM_ID, log_message)

# Function to handle all incoming messages (not only commands)
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    # Log all user interactions
    log_message = f"User {user_id} sent: {message.text}"
    bot.send_message(MY_TELEGRAM_ID, log_message)

# Start polling the bot
bot.polling()
