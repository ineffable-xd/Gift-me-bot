from telegram import Bot

# Your Telegram Bot Token (Replace this with your bot's token)
API_TOKEN = '7571171685:AAG-cbHDHzGq-bossU-lzG2uVLxLNc-YIRM'

# Your Telegram Chat ID (You provided this as 1972239827)
CHAT_ID = 1972239827

def send_hello_message():
    # Initialize the bot with the API token
    bot = Bot(token=API_TOKEN)
    
    # Send the "Hello" message to your Telegram DM
    bot.send_message(chat_id=CHAT_ID, text="Hello")

if __name__ == "__main__":
    send_hello_message()
