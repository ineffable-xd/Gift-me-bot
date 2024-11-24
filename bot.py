import os
import random
import time
import telebot
import traceback

# Use the Telegram API token from Scalingo environment variable
TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')

# Check if the token is available
if TELEGRAM_API_TOKEN is None:
    raise ValueError("TELEGRAM_API_TOKEN is not set")

# Initialize the bot
bot = telebot.TeleBot(TELEGRAM_API_TOKEN)

# Telegram chat ID for logging purposes (change this to the chat ID you want to send logs to)
LOG_CHAT_ID = 'YOUR_CHAT_ID'  # Replace with your chat ID

# List of gift links (replace with actual gift links)
GIFTS = [
    "https://raw.githubusercontent.com/ineffable-xd/Gift-me-bot/refs/heads/main/gifts/gift1.tex"
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

# Function to send log messages to Telegram (for debugging)
def send_log_to_telegram(log_message):
    try:
        bot.send_message(LOG_CHAT_ID, log_message)
    except Exception as e:
        print(f"Error sending log to Telegram: {e}")

# Command to send a random gift link
@bot.message_handler(commands=['giftme'])
def handle_giftme(message):
    try:
        user_id = message.chat.id
        send_log_to_telegram(f"Received /giftme command from user: {user_id}")
        
        # Initialize counter for the user if not already done
        if user_id not in gift_counter:
            gift_counter[user_id] = 0
            send_log_to_telegram(f"Gift counter for user {user_id} initialized.")
        
        if gift_counter[user_id] < 6:
            send_log_to_telegram(f"User {user_id} has requested gift #{gift_counter[user_id] + 1}.")
            
            # Ensure the GIFTS list is not empty
            if not GIFTS:
                bot.send_message(user_id, "Sorry, no gifts are available right now.")
                send_log_to_telegram("GIFTS list is empty, no gift to send.")
                return
                
            # Send a random gift link from the GIFTS list
            gift = random.choice(GIFTS)
            bot.send_message(user_id, f"Here's your gift: {gift}")
            gift_counter[user_id] += 1
            send_log_to_telegram(f"Sent gift to user {user_id}: {gift}. Gift count: {gift_counter[user_id]}")
        else:
            # After 6 requests, send a random message from the RANDOM_MESSAGES list
            random_message = random.choice(RANDOM_MESSAGES)
            bot.send_message(user_id, random_message)
            send_log_to_telegram(f"User {user_id} has reached gift limit. Sent random message: {random_message}")
    
    except Exception as e:
        error_message = f"Error in handle_giftme for user {message.chat.id}: {e}\n{traceback.format_exc()}"
        send_log_to_telegram(error_message)
        bot.send_message(message.chat.id, "An error occurred, please try again later.")
        
# Command to reset the gift counter (for testing purposes)
@bot.message_handler(commands=['reset'])
def reset_gift_counter(message):
    try:
        user_id = message.chat.id
        gift_counter[user_id] = 0
        bot.send_message(user_id, "Your gift counter has been reset. You can now request gifts again!")
        send_log_to_telegram(f"Gift counter for user {user_id} has been reset.")
    except Exception as e:
        error_message = f"Error in reset_gift_counter for user {message.chat.id}: {e}\n{traceback.format_exc()}"
        send_log_to_telegram(error_message)
        bot.send_message(message.chat.id, "An error occurred, please try again later.")
        
# Function to start the bot and keep it running indefinitely
def run_bot():
    while True:
        try:
            # Start polling the bot to keep it active
            send_log_to_telegram("Starting bot polling...")
            print("Bot started...")
            bot.polling(none_stop=True, interval=0)
        except Exception as e:
            # If an error occurs, log it and restart the bot after a delay
            error_message = f"Error occurred in bot polling: {e}\n{traceback.format_exc()}"
            send_log_to_telegram(error_message)
            time.sleep(5)  # Wait for 5 seconds before restarting

if __name__ == "__main__":
    run_bot()
