import os
import random
import time
import telebot

# Use the Telegram API token from Scalingo environment variable
TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')

# Check if the token is available
if TELEGRAM_API_TOKEN is None:
    raise ValueError("TELEGRAM_API_TOKEN is not set")

# Initialize the bot
bot = telebot.TeleBot(TELEGRAM_API_TOKEN)

# List of gift links (replace with actual gift links)
GIFTS = [
    "https://raw.githubusercontent.com/ineffable-xd/Gift-me-bot/refs/heads/main/gifts/gift1.tex"
    # Add more gift links here
]

# Check if the GIFTS list is not empty
if not GIFTS:
    raise ValueError("GIFTS list is empty, add some gift links")

# List of random messages (replace with actual random messages)
RANDOM_MESSAGES = [
    "Thank you for using the bot!",
    "Hope you're having a great day!",
    "Keep smiling, you're awesome!",
    "Stay positive and keep going!",
    "Life is good, enjoy it!",
    "You're doing great, keep it up!"
    # Add more random messages here
]

# Initialize a counter to track how many times a user has requested gifts
gift_counter = {}

# Command to send a random gift link
@bot.message_handler(commands=['giftme'])
def handle_giftme(message):
    user_id = message.chat.id
    
    # Initialize counter for the user if not already done
    if user_id not in gift_counter:
        gift_counter[user_id] = 0

    if gift_counter[user_id] < 6:
        try:
            # Ensure the GIFTS list is not empty
            if not GIFTS:
                bot.send_message(user_id, "Sorry, no gifts are available right now.")
                return
            # Send a random gift link from the GIFTS list
            gift = random.choice(GIFTS)
            bot.send_message(user_id, f"Here's your gift: {gift}")
            gift_counter[user_id] += 1
        except Exception as e:
            bot.send_message(user_id, f"An error occurred while fetching a gift: {e}")
    else:
        # After 6 requests, send a random message from the RANDOM_MESSAGES list
        random_message = random.choice(RANDOM_MESSAGES)
        bot.send_message(user_id, random_message)

# Command to reset the gift counter (for testing purposes)
@bot.message_handler(commands=['reset'])
def reset_gift_counter(message):
    user_id = message.chat.id
    gift_counter[user_id] = 0
    bot.send_message(user_id, "Your gift counter has been reset. You can now request gifts again!")

# Function to start the bot and keep it running indefinitely
def run_bot():
    while True:
        try:
            # Start polling the bot to keep it active
            print("Bot started...")
            bot.polling(none_stop=True, interval=0)
        except Exception as e:
            # If an error occurs, log it and restart the bot after a delay
            print(f"Error occurred: {e}")
            time.sleep(5)  # Wait for 5 seconds before restarting

if __name__ == "__main__":
    run_bot()
