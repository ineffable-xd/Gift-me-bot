import os
import random
import telebot

# Get the bot token from the environment variable
TOKEN = os.getenv('TOKEN')
USER_ID = 1972239827  # Your Telegram user ID

# List of gift links to be sent
gift_links = [
    "https://example.com/gift1",
    "https://example.com/gift2",
    "https://example.com/gift3",
    "https://example.com/gift4",
    "https://example.com/gift5",
    "https://example.com/gift6",
    "https://example.com/gift7",
]

# Random text to send after 6 gifts
random_text = [
    "Here's a little surprise for you! 🎁",
    "You deserve something special today! 💫",
    "Hope this brightens your day! ✨",
    "Enjoy your gift! 🎉",
    "A small token of appreciation for you! 💖",
    "You're awesome! Here's a surprise! 💌",
]

# Track how many times the user has received gifts
user_gift_count = {}

# Initialize the bot
bot = telebot.TeleBot(TOKEN)

# Send logs to your Telegram account
def send_log(message: str):
    bot.send_message(chat_id=USER_ID, text=message)

# Command to send gifts or random messages
@bot.message_handler(commands=['surprise', 'giftme'])
def send_gift(message):
    user_id = message.chat.id

    # Initialize gift count if user is new
    if user_id not in user_gift_count:
        user_gift_count[user_id] = 0

    # Check if the user has received 6 gifts already
    if user_gift_count[user_id] < 6:
        # Send a gift link
        gift_link = random.choice(gift_links)
        bot.reply_to(message, gift_link)
        user_gift_count[user_id] += 1
        send_log(f"Gift sent to {user_id}: {gift_link}")
    else:
        # Send a random message from random_text after 6 gifts
        random_message = random.choice(random_text)
        bot.reply_to(message, random_message)
        user_gift_count[user_id] = 0  # Reset the gift count after sending the random message
        send_log(f"Random message sent to {user_id}: {random_message}")

# Notify when the bot starts
send_log("Bot started successfully!")

# Start polling to listen for messages
bot.polling()
