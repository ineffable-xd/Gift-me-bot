import telebot
import time

# Replace 'YOUR_TOKEN' with your actual Telegram Bot token
API_TOKEN = 'YOUR_TOKEN'

bot = telebot.TeleBot(API_TOKEN)

# Command handler for /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello, I am your bot! How can I assist you today?")

# Polling loop to keep the bot running
while True:
    try:
        bot.polling(non_stop=True)
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(15)  # Wait for a while before trying again
