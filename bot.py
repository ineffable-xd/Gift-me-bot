import telebot
import random
import json
import os
import requests

# Access the Telegram API token from the environment variable
TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')

if TELEGRAM_API_TOKEN is None:
    raise ValueError("TELEGRAM_API_TOKEN is not set")

# Initialize the bot
bot = telebot.TeleBot(TELEGRAM_API_TOKEN)

# URL of your gifts.json on GitHub
GIFTS_JSON_URL = 'https://raw.githubusercontent.com/ineffable-xd/Gift-me-bot/refs/heads/main/gifts.json'

# Function to load gifts from the GitHub URL
def load_gifts():
    try:
        response = requests.get(GIFTS_JSON_URL)
        response.raise_for_status()  # Check if the request was successful
        return response.json()  # Return the JSON response as a list of gifts
    except requests.exceptions.RequestException as e:
        print(f"Error loading gifts: {e}")
        return []

# Function to load random messages
def load_random_messages():
    random_messages_url = 'https://raw.githubusercontent.com/ineffable-xd/Gift-me-bot/refs/heads/main/random_messages.txt'
    try:
        response = requests.get(random_messages_url)
        response.raise_for_status()  # Check if the request was successful
        return response.text.splitlines()  # Return the text as a list of messages
    except requests.exceptions.RequestException as e:
        print(f"Error loading random messages: {e}")
        return []

# Initialize a counter to track the number of gifts sent
gift_counter = {}

# Command to send random gift
@bot.message_handler(commands=['giftme'])
def handle_giftme(message):
    user_id = message.chat.id
    if user_id not in gift_counter:
        gift_counter[user_id] = 0

    if gift_counter[user_id] < 6:
        gifts = load_gifts()
        if gifts:
            gift = random.choice(gifts)
            bot.send_message(user_id, f"Here's your gift: {gift}")
            gift_counter[user_id] += 1
        else:
            bot.send_message(user_id, "Sorry, no gifts available at the moment.")
    else:
        random_messages = load_random_messages()
        if random_messages:
            random_message = random.choice(random_messages)
            bot.send_message(user_id, random_message)
        else:
            bot.send_message(user_id, "Sorry, I'm out of random messages for now.")

# Command to reset the gift counter (for testing purposes)
@bot.message_handler(commands=['reset'])
def reset_gift_counter(message):
    user_id = message.chat.id
    gift_counter[user_id] = 0
    bot.send_message(user_id, "Your gift counter has been reset.")

# Start the bot
bot.polling(none_stop=True)
