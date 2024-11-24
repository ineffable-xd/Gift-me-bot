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
    try:
        print("Received /hello command")  # Debugging message
        bot.send_message(message.chat.id, "Hello there! How can I assist you today?")
    except Exception as e:
        print(f"Error in /hello handler: {e}")
        bot.send_message(message.chat.id, "Sorry, something went wrong.")

# Command handler for /hi
@bot.message_handler(commands=["hi"])
def hi(message):
    try:
        print("Received /hi command")  # Debugging message
        bot.send_message(message.chat.id, "Hi! How's it going?")
    except Exception as e:
        print(f"Error in /hi handler: {e}")
        bot.send_message(message.chat.id, "Sorry, something went wrong.")

# Command handler for /giftme
@bot.message_handler(commands=["giftme"])
def giftme(message):
    global gift_count
    try:
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
    except Exception as e:
        print(f"Error in /giftme handler: {e}")
        bot.send_message(message.chat.id, "Sorry, something went wrong with your gift.")

# Command handler for /reset
@bot.message_handler(commands=["reset"])
def reset(message):
    global gift_count
    try:
        gift_count = 0
        print("Gift count reset to 0")  # Debugging message
        bot.send_message(message.chat.id, "Gift count has been reset for the day.")
    except Exception as e:
        print(f"Error in /reset handler: {e}")
        bot.send_message(message.chat.id, "Sorry, something went wrong while resetting the gift count.")

# Start command for debugging
@bot.message_handler(commands=["start"])
def start(message):
    try:
        print("Received /start command")  # Debugging message
        bot.send_message(message.chat.id, "Bot is running successfully!")
    except Exception as e:
        print(f"Error in /start handler: {e}")
        bot.send_message(message.chat.id, "Sorry, something went wrong during bot startup.")

# Error handling to log any unexpected issues
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    try:
        print(f"Received message: {message.text}")  # Debugging message
    except Exception as e:
        print(f"Error handling message: {e}")

# Run the bot
if __name__ == "__main__":
    try:
        print("Bot starting...")  # Debugging message
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Error starting bot: {e}")
