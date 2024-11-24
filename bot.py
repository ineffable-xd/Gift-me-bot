import os
import random
import telebot
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

# Command handler for /hello
@bot.message_handler(commands=["hello"])
def hello(message):
    print("Received /hello command")  # Debugging message
    bot.send_message(message.chat.id, "Hello there! How can I assist you today?")

# Command handler for /hi
@bot.message_handler(commands=["hi"])
def hi(message):
    print("Received /hi command")  # Debugging message
    bot.send_message(message.chat.id, "Hi! How's it going?")

# Command handler for /giftme
@bot.message_handler(commands=["giftme"])
def giftme(message):
    global gift_count
    print("Received /giftme command")  # Debugging message

    # Check if the user has reached the daily limit
    if gift_count < max_gifts_per_day:
        gift_count += 1
        # Simulating a gift (for debugging)
        gift = "Random Wallpaper"
        print(f"Sending gift: {gift}")  # Debugging message
        bot.send_message(message.chat.id, f"Here’s your gift! {gift}")
    else:
        # Send a random message from the file
        with open(RANDOM_MESSAGES_FILE, "r") as f:
            random_messages = f.read().splitlines()
        print("Sending random message from file")  # Debugging message
        bot.send_message(message.chat.id, random.choice(random_messages))

# Command handler for /reset
@bot.message_handler(commands=["reset"])
def reset(message):
    global gift_count
    gift_count = 0
    print("Gift count reset to 0")  # Debugging message
    bot.send_message(message.chat.id, "Gift count has been reset for the day.")

# Start command for debugging
@bot.message_handler(commands=["start"])
def start(message):
    print("Received /start command")  # Debugging message
    bot.send_message(message.chat.id, "Bot is running successfully!")

# Error handling to log any unexpected issues
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    print(f"Received message: {message.text}")  # Debugging message

# Run the bot
if __name__ == "__main__":
    print("Bot starting...")  # Debugging message
    bot.polling(none_stop=True)
