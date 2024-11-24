import os
import random
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
        # Send a random gift link from the GIFTS list
        gift = random.choice(GIFTS)
        bot.send_message(user_id, f"Here's your gift: {gift}")
        gift_counter[user_id] += 1
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

# Start the bot
bot.polling(none_stop=True)
