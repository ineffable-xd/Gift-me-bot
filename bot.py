import telebot
import random
import logging
import time
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

API_TOKEN = '7571171685:AAG-cbHDHzGq-bossU-lzG2uVLxLNc-YIRM'  # Your bot API token
MY_TELEGRAM_ID = 1972239827  # Your Telegram ID

bot = telebot.TeleBot(API_TOKEN)

# Define the random messages
RANDOM_MESSAGES_FILE = [
    "Hope you have a great day!",
    "Don't forget to smile!",
    "Keep up the good work!",
    "Stay positive!",
    "You're doing amazing!",
    "Believe in yourself!"
]

# Define the gift list
GIFTS = [
    "http://example.com/gift1",  # Gift 1 URL
    "http://example.com/gift2",  # Gift 2 URL
    "http://example.com/gift3",  # Gift 3 URL
    "http://example.com/gift4",  # Gift 4 URL
    "http://example.com/gift5",  # Gift 5 URL
    "http://example.com/gift6"   # Gift 6 URL
]

# Initialize the user gift counter and logs
user_gift_count = {}
user_logs = []

# Function to send logs to the admin
def send_log_to_admin(message):
    bot.send_message(MY_TELEGRAM_ID, message)

# Function to reset the gift count at midnight
def reset_gift_count():
    global user_gift_count
    user_gift_count = {}
    send_log_to_admin("Gift count has been reset for all users.")

# Schedule the reset function
scheduler = BackgroundScheduler()
scheduler.add_job(reset_gift_count, 'cron', hour=0, minute=0)  # Runs at midnight every day
scheduler.start()

# Handle /gift_me and /surprise commands
@bot.message_handler(commands=['gift_me', 'surprise'])
def handle_gift(message):
    user_id = message.from_user.id
    text = message.text.lower()

    if user_id not in user_gift_count:
        user_gift_count[user_id] = 0

    if user_gift_count[user_id] < 6:
        # Send a gift from the list
        gift_index = user_gift_count[user_id]
        gift_link = GIFTS[gift_index]  # Select the corresponding gift
        bot.send_message(user_id, f"Here is your gift: {gift_link}")
        user_gift_count[user_id] += 1
    else:
        # Send a random message after 6 gifts
        random_message = random.choice(RANDOM_MESSAGES_FILE)
        bot.send_message(user_id, random_message)

    # Log the interaction
    log_message = f"User {user_id} ({message.from_user.first_name}) sent '{message.text}' and received: '{gift_link if user_gift_count[user_id] < 6 else random_message}'"
    user_logs.append(log_message)
    send_log_to_admin(log_message)

# Handle all other messages
@bot.message_handler(func=lambda message: True)
def log_all_messages(message):
    log_message = f"User {message.from_user.id} ({message.from_user.first_name}) sent: '{message.text}'"
    user_logs.append(log_message)
    send_log_to_admin(log_message)

# Polling to keep the bot running
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        time.sleep(15)
