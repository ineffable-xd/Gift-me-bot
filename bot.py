import os
import random
import telebot
import json
from google_drive import get_drive_files
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Bot setup
TOKEN = os.getenv("TELEGRAM_API_TOKEN")
bot = telebot.TeleBot(TOKEN)

# Limit for gifts per day
gift_count = 0
max_gifts_per_day = 10

# File with random messages
RANDOM_MESSAGES_FILE = os.getenv("RANDOM_MESSAGES_FILE")

# Command handler for /giftme
@bot.message_handler(commands=["giftme"])
def giftme(message):
    global gift_count

    # Check if the user has reached the daily limit
    if gift_count < max_gifts_per_day:
        gift_count += 1
        files = get_drive_files()
        random_file = random.choice(files)
        bot.send_message(message.chat.id, f"Here’s your gift! {random_file}")
    else:
        # Send a random message from the file
        with open(RANDOM_MESSAGES_FILE, "r") as f:
            random_messages = f.read().splitlines()
        bot.send_message(message.chat.id, random.choice(random_messages))

# Command handler for /reset
@bot.message_handler(commands=["reset"])
def reset(message):
    global gift_count
    gift_count = 0
    bot.send_message(message.chat.id, "Gift count has been reset for the day.")

# Run the bot
if __name__ == "__main__":
    bot.polling(none_stop=True)
