import os
import random
import telebot
from flask import Flask, request

# Get the bot token and user ID from environment variables
TOKEN = os.getenv('TOKEN')
USER_ID = 1972239827  # Your Telegram user ID to send logs to

if not TOKEN:
    raise ValueError("TOKEN environment variable not set!")

# Initialize the bot
bot = telebot.TeleBot(TOKEN)

# Flask app for webhook
app = Flask(__name__)

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

# Send logs to your Telegram account
def send_log(message):
    try:
        bot.send_message(USER_ID, f"[LOG]: {message}")
    except Exception as e:
        print(f"Failed to send log: {e}")

# Command to handle /giftme and /surprise
@bot.message_handler(commands=["giftme", "surprise"])
def send_gift(message):
    user_id = message.chat.id

    # Initialize gift count if user is new
    if user_id not in user_gift_count:
        user_gift_count[user_id] = 0

    # Log gift request
    send_log(f"User {user_id} requested a gift.")

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
        user_gift_count[user_id] = 0  # Reset the gift count
        send_log(f"Random message sent to {user_id}: {random_message}")

# Webhook route
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "OK", 200

# Set webhook on startup
@app.before_first_request
def setup_webhook():
    webhook_url = f"https://{os.getenv('SCALINGO_APP_NAME')}.scalingo.io/{TOKEN}"
    bot.remove_webhook()
    bot.set_webhook(url=webhook_url)
    send_log(f"Webhook set to {webhook_url}")

# Start the Flask app
if __name__ == "__main__":
    send_log("Bot is starting...")
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
