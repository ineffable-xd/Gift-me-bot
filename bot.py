import os
import random
import telebot
import requests
import json
from datetime import datetime

# Retrieve the Telegram Bot Token from environment variables
TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')
if not TELEGRAM_API_TOKEN:
    raise ValueError("Telegram bot token not found in environment variables.")

# Initialize the bot
bot = telebot.TeleBot(TELEGRAM_API_TOKEN)

# URL of the JSON file containing gifts and random messages
GIFTS_JSON_URL = "https://raw.githubusercontent.com/ineffable-xd/Gift-me-bot/refs/heads/main/gifts.json"
RANDOM_MESSAGES_URL = "https://raw.githubusercontent.com/ineffable-xd/Gift-me-bot/refs/heads/main/random_messages.txt"

# Store the used gifts count (you may need to use a persistent storage like a database in production)
user_gift_count = {}

# Function to fetch gifts from the GitHub repo
def fetch_gifts():
    try:
        response = requests.get(GIFTS_JSON_URL)
        response.raise_for_status()  # Check if the request was successful
        gifts = response.json()
        return gifts
    except requests.RequestException as e:
        print(f"Error fetching gifts: {e}")
        return []

# Function to fetch random messages from GitHub repo
def fetch_random_messages():
    try:
        response = requests.get(RANDOM_MESSAGES_URL)
        response.raise_for_status()  # Check if the request was successful
        messages = response.text.splitlines()
        return messages
    except requests.RequestException as e:
        print(f"Error fetching random messages: {e}")
        return []

# Send a random gift to the user
def send_random_gift(message):
    user_id = message.chat.id
    
    # Check if the user has already received a gift 6 times today
    today = datetime.now().date()
    if user_id not in user_gift_count:
        user_gift_count[user_id] = {"count": 0, "date": today}
    
    if user_gift_count[user_id]["date"] == today and user_gift_count[user_id]["count"] >= 6:
        bot.send_message(user_id, "You have already received your daily limit of 6 gifts. Please try again tomorrow.")
        return
    
    # Fetch the gifts and select a random one
    gifts = fetch_gifts()
    if not gifts:
        bot.send_message(user_id, "Sorry, no gifts available at the moment.")
        return
    
    gift = random.choice(gifts)
    gift_name = gift.get('name', 'Unknown Gift')
    gift_link = gift.get('link', '')
    
    # Send the gift to the user
    bot.send_message(user_id, f"Here is your random gift: {gift_name}\nLink: {gift_link}")
    
    # Increment gift count for today
    user_gift_count[user_id]["count"] += 1

# Send a random message to the user
def send_random_message(message):
    user_id = message.chat.id
    messages = fetch_random_messages()
    if not messages:
        bot.send_message(user_id, "Sorry, no random messages available at the moment.")
        return
    
    random_message = random.choice(messages)
    bot.send_message(user_id, random_message)

# Command to trigger the random gift
@bot.message_handler(commands=['giftme'])
def handle_giftme(message):
    send_random_gift(message)

# Command to trigger a random message (in case the user uses all 6 gifts)
@bot.message_handler(commands=['randommessage'])
def handle_random_message(message):
    send_random_message(message)

# Start the bot
if __name__ == "__main__":
    print("Bot started.")
    bot.polling()
