import os
import random
import telebot
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Bot setup
TOKEN = os.getenv("TELEGRAM_API_TOKEN")
bot = telebot.TeleBot(TOKEN)

# Telegram user ID to send messages to (replace with your user ID)
TELEGRAM_USER_ID = os.getenv("TELEGRAM_USER_ID")

# File with random messages
RANDOM_MESSAGES_FILE = os.getenv("RANDOM_MESSAGES_FILE")

# Function to authenticate Google Drive and send status to Telegram DM
def authenticate_google_drive():
    try:
        credentials, project = google.auth.load_credentials_from_file(os.getenv("GOOGLE_CREDENTIALS"))
        drive_service = build("drive", "v3", credentials=credentials)
        
        # Testing if we can retrieve files from the drive
        folder_id = os.getenv("FOLDER_ID")
        query = f"'{folder_id}' in parents"
        results = drive_service.files().list(q=query).execute()
        files = results.get("files", [])
        
        # Send success message to Telegram DM
        bot.send_message(TELEGRAM_USER_ID, "Successfully authenticated with Google Drive!")
        print(f"Authenticated as project: {project}")
        return True

    except google.auth.exceptions.DefaultCredentialsError as e:
        # Send failure message to Telegram DM
        bot.send_message(TELEGRAM_USER_ID, f"Google Drive authentication failed: {e}")
        print(f"Google authentication failed: {e}")
        return False
    except HttpError as e:
        # Send failure message to Telegram DM
        bot.send_message(TELEGRAM_USER_ID, f"Google Drive API error: {e}")
        print(f"Google API error: {e}")
        return False
    except Exception as e:
        # Handle any other errors
        bot.send_message(TELEGRAM_USER_ID, f"An error occurred while authenticating: {e}")
        print(f"An error occurred: {e}")
        return False

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
    print("Received /giftme command")  # Debugging message

    # Simulating a gift (for debugging)
    gift = "Random Wallpaper"
    print(f"Sending gift: {gift}")  # Debugging message
    bot.send_message(message.chat.id, f"Here’s your gift! {gift}")

# Command handler for /start
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
    
    # Authenticate with Google Drive and send login status to Telegram DM
    authenticate_google_drive()

    bot.polling(none_stop=True)
