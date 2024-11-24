import telebot
from datetime import datetime
import random

API_TOKEN = os.getenv('TOKEN')
bot = telebot.TeleBot(API_TOKEN)

# Variables to store data
user_gift_count = {}
reset_time = datetime.now().date()
gift_links = [
    "https://example.com/gift1",
    "https://example.com/gift2",
    "https://example.com/gift3",
    "https://example.com/gift4",
    "https://example.com/gift5",
    "https://example.com/gift6"
]
random_text = [
    "Better luck tomorrow!",
    "That's all the gifts for today!",
    "Come back tomorrow for more gifts!",
    "Today's gifts are finished. Try again tomorrow!"
]

# Customizable responses
custom_responses = {
    'welcome_message': "Welcome to the Gift Bot! Use /giftme to get your daily gifts.",
    'limit_reached_message': "You’ve already received all your gifts for today.",
    'gift_reset_message': "Gifts have been reset for the day! You can try again now."
}

# Reset function
def reset_gift_count():
    global user_gift_count, reset_time
    current_date = datetime.now().date()
    if reset_time != current_date:
        user_gift_count = {}
        reset_time = current_date

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, custom_responses['welcome_message'])

@bot.message_handler(commands=['giftme'])
def send_gift(message):
    reset_gift_count()
    user_id = message.from_user.id
    
    # Check if the user has reached their limit
    if user_id not in user_gift_count:
        user_gift_count[user_id] = 0
    
    if user_gift_count[user_id] < 6:
        gift = gift_links[user_gift_count[user_id] % len(gift_links)]
        bot.reply_to(message, gift)
        user_gift_count[user_id] += 1
    else:
        bot.reply_to(message, random.choice(random_text))
        
@bot.message_handler(commands=['reset'])
def reset_command(message):
    reset_gift_count()
    bot.reply_to(message, custom_responses['gift_reset_message'])

bot.polling()
