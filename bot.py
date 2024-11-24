import requests
import random
import telebot
from datetime import datetime

# Your bot token
BOT_TOKEN = TELEGRAM_API_TOKEN
bot = telebot.TeleBot(BOT_TOKEN)

# Replace with your Telegram user or chat ID
TELEGRAM_USER_ID = "1972239827"

# GitHub URLs for gifts and random messages
GIFTS_JSON_URL = "https://raw.githubusercontent.com/ineffable-xd/Gift-me-bot/refs/heads/main/gifts.json"
MESSAGES_TXT_URL = "https://raw.githubusercontent.com/ineffable-xd/Gift-me-bot/refs/heads/main/random_messages.txt"

# Tracking gift counts per user (daily limit)
user_gift_counts = {}
max_gifts_per_day = 6

# Fetch text file content (random messages)
def fetch_text_file(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text.splitlines()
    except requests.RequestException as e:
        print(f"Error fetching text file: {e}")
        return []

# Fetch JSON data (gifts list)
def fetch_json(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching JSON data: {e}")
        return None

# Fetch random gift from GitHub
def fetch_random_gift():
    gifts_data = fetch_json(GIFTS_JSON_URL)
    if gifts_data and "gifts" in gifts_data:
        return random.choice(gifts_data["gifts"])
    return None

# Fetch random message from the text file
def fetch_random_message():
    messages = fetch_text_file(MESSAGES_TXT_URL)
    if messages:
        return random.choice(messages)
    return "Keep shining! 🌟"

# Command to handle /giftme
@bot.message_handler(commands=['giftme'])
def handle_gift_request(message):
    global user_gift_counts

    # Get the user ID and check how many gifts they have received today
    user_id = message.from_user.id
    today_date = datetime.today().date()

    # Initialize or reset count for the user on a new day
    if user_id not in user_gift_counts or user_gift_counts[user_id]["date"] != today_date:
        user_gift_counts[user_id] = {"count": 0, "date": today_date}

    # Check if the user has already reached the daily gift limit
    if user_gift_counts[user_id]["count"] >= max_gifts_per_day:
        # Send a random message instead of a gift
        random_message = fetch_random_message()
        bot.send_message(user_id, random_message)
        return

    # Otherwise, send a random gift
    random_gift = fetch_random_gift()
    if random_gift:
        gift_url = random_gift["link"]
        bot.send_message(user_id, f"Here is your gift: {gift_url}")
        
        # Update the user's gift count for the day
        user_gift_counts[user_id]["count"] += 1
    else:
        bot.send_message(user_id, "Sorry, no gifts are available right now.")

# Function to reset daily counts (optional, for maintenance purposes)
def reset_daily_counts():
    global user_gift_counts
    user_gift_counts = {}

# Start the bot
if __name__ == '__main__':
    bot.polling(none_stop=True)
