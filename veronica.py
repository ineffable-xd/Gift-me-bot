import telebot
import random

# Telegram bot token and your Telegram ID
API_TOKEN = '7571171685:AAG-cbHDHzGq-bossU-lzG2uVLxLNc-YIRM'
MY_TELEGRAM_ID = '1972239827'

# Create the bot instance
bot = telebot.TeleBot(API_TOKEN)

# Define quotes based on percentage ranges (for IQ)
def generate_quote(percentage):
    if percentage <= 5:
        return "You're a total waste of space."
    elif 6 <= percentage <= 10:
        return "Seriously, how did you even manage to exist this far?"
    elif 11 <= percentage <= 15:
        return "Just stop, you're embarrassing yourself."
    elif 16 <= percentage <= 20:
        return "This is painful to witness."
    elif 21 <= percentage <= 25:
        return "Barely scraping by. It’s sad."
    elif 26 <= percentage <= 30:
        return "Focus, because you're not even trying."
    elif 31 <= percentage <= 35:
        return "You're on the struggle bus, no brakes."
    elif 36 <= percentage <= 40:
        return "Pretty much useless at this point."
    elif 41 <= percentage <= 45:
        return "Half-assed attempt. Try harder."
    elif 46 <= percentage <= 50:
        return "You're kinda trying, but it's still embarrassing."
    elif 51 <= percentage <= 55:
        return "Not too bad, but you’re still way behind."
    elif 56 <= percentage <= 60:
        return "You're getting there, but not quite."
    elif 61 <= percentage <= 65:
        return "Improving, but still kinda dumb."
    elif 66 <= percentage <= 69:
        return "Getting better, but not by much."
    elif 70 <= percentage <= 75:
        return "You're doing well now, but stop slacking."
    elif 76 <= percentage <= 80:
        return "Actually impressive now, wow!"
    elif 81 <= percentage <= 85:
        return "You’re doing pretty damn well!"
    elif 86 <= percentage <= 90:
        return "Damn, you're smart! Respect."
    elif 91 <= percentage <= 95:
        return "Top-tier intellect. You're elite."
    elif 96 <= percentage <= 100:
        return "You're basically a genius. Damn, I’m impressed!"

# Define roast quotes
def generate_roast(user_name):
    roasts = [
       "Listen, your brain is like a software update. It takes forever to process and it never works right.",
        "Listen, you're like a cloud storage account—always full of nothing.",
        "Listen, calling you an idiot would be an insult to stupid people.",
        "Listen, if your IQ was any lower, we’d have to water you.",
        "Listen, you make a rock look like a genius.",
        "Listen, you're proof that some people can’t even handle a single task properly.",
        "Listen, your existence is a constant reminder that life doesn’t always get it right.",
        "Listen, you’re a living, breathing example of wasted potential.",
        "Listen, if there were a prize for incompetence, you’d be the reigning champion.",
        "Listen, you’re the reason they put instructions on shampoo bottles.",
        "Listen, your brain is like a slow-loading website — completely useless until it finally gives up.",
        "Listen, if stupidity was a crime, you’d be serving a life sentence.",
        "Listen, you’re like a car with no engine — all looks and no function.",
        "Listen, if there was an award for being completely useless, you’d win every year.",
        "Listen, your IQ is so low, it’s practically a negative number.",
        "Listen, you’re proof that even the worst ideas get a chance to exist.",
        "Listen, you’re not even the smartest in your family of amoebas.",
        "Listen, you make a paper bag look like it has more personality.",
        "Listen, you couldn’t outsmart a traffic light.",
        "Listen, if you were any dumber, we’d have to start putting warning labels on you.",
        "Listen, if I had a dollar for every brain cell you have, I’d be broke.",
        "Listen, you’re like a malfunctioning vending machine — a waste of space.",
        "Listen, you couldn’t even pass a test on basic survival.",
        "Listen, the only thing you’re good at is disappointing everyone around you.",
        "Listen, you’d be a complete failure if it weren’t for the fact that you don’t even try.",
        "Listen, you’re not a person, you’re just a mistake that refuses to go away.",
        "Listen, you make a brick look like a genius.",
        "Listen, your brain is like a broken calculator — completely useless.",
        "Listen, you’re like a low-budget horror movie — everyone wants to leave after 5 minutes.",
        "Listen, even a broken clock is smarter than you.",
        "Listen, your life’s biggest achievement is making other people feel superior.",
        "Listen, if ignorance is bliss, you must be the happiest person alive.",
        "Listen, your intelligence is like a fart — everyone knows it’s there, but no one wants to acknowledge it.",
        "Listen, you’re not even a blip on the radar of success.",
        "Listen, you’re the kind of person who would fail a test on 'How to Be a Human Being.'",
        "Listen, your thoughts are so empty, I’m surprised they don’t echo.",
        "Listen, if you ever achieve greatness, it’ll be because someone else did all the work.",
        "Listen, your brain is so empty, even a vacuum cleaner is jealous.",
        "Listen, if brains were taxed, you’d get a refund.",
        "Listen, you could stand in a field of dumb and still be the dumbest thing there.",
        "Listen, you’re proof that the world would be better off without some people.",
        "Listen, you make the word ‘useless’ seem like a compliment.",
        "Listen, if there was a championship for failing, you’d have a trophy case full of them.",
        "Listen, if you were any less self-aware, we’d have to start charging for your lack of consciousness.",
        "Listen, you’re the human equivalent of a participation trophy.",
        "Listen, even the mirror is embarrassed to reflect you.",
        "Listen, you bring absolutely nothing to the table, except maybe a napkin.",
        "Listen, your only talent is managing to be consistently disappointing.",
        "Listen, you have the personality of a damp sponge.",
        "Listen, you’re the living embodiment of ‘Why even try?’",
        "Listen, you’re the type of person who can’t even finish a sentence without ruining it.",
        "Listen, you’re like a slow Wi-Fi signal — everyone around you is just waiting for you to stop existing.",
        "Listen, even a brick wall has more value than you.",
        "Listen, you’re not the sharpest tool in the shed, you’re the one everyone forgets about.",
        "Listen, you’ve achieved absolutely nothing in life and that’s honestly impressive.",
        "Listen, you could be the smartest person in the room, but unfortunately, the room is full of rocks.",
        "Listen, your presence is about as necessary as a screen door on a submarine."
    ]
    return random.choice(roasts)

# Function to log activity
def log_to_owner(user, command, response):
    log_message = f"User: {user.first_name} ({user.id})\nCommand: {command}\nResponse: {response}"
    bot.send_message(MY_TELEGRAM_ID, log_message)

# Command to generate and send a random IQ percentage and quote
@bot.message_handler(commands=['iq'])
def handle_iq_level(message):
    command = message.text
    user_id = message.from_user.id
    user_first_name = message.from_user.first_name

    # If the user replies to someone
    if message.reply_to_message:
        replied_user = message.reply_to_message.from_user
        replied_user_id = replied_user.id
        replied_user_name = replied_user.first_name
        random_percentage = random.randint(0, 100)
        quote = generate_quote(random_percentage)
        response = f"Hey <a href='tg://user?id={replied_user_id}'>{replied_user_name}</a>, your IQ level is: {random_percentage}%\n{quote}"
        bot.send_message(message.chat.id, response, parse_mode="HTML")
        log_to_owner(message.from_user, command, response)

    # If the user mentions someone with @username
    elif '@' in command:
        username = command.split('@')[1].strip()
        random_percentage = random.randint(0, 100)
        quote = generate_quote(random_percentage)
        response = f"Hey @{username}, your IQ level is: {random_percentage}%\n{quote}"
        bot.send_message(message.chat.id, response, parse_mode="HTML")
        log_to_owner(message.from_user, command, response)

    # If the user types /iq_level without replying or mentioning
    else:
        random_percentage = random.randint(0, 100)
        quote = generate_quote(random_percentage)
        response = f"Hey <a href='tg://user?id={user_id}'>{user_first_name}</a>, your IQ level is: {random_percentage}%\n{quote}"
        bot.send_message(message.chat.id, response, parse_mode="HTML")
        log_to_owner(message.from_user, command, response)

# Command to generate and send a random roast
@bot.message_handler(commands=['roast'])
def handle_roast(message):
    command = message.text
    user_id = message.from_user.id
    user_first_name = message.from_user.first_name

    # If the user replies to someone
    if message.reply_to_message:
        replied_user = message.reply_to_message.from_user
        replied_user_name = replied_user.first_name
        roast = generate_roast(replied_user_name)
        response = f"Hey <a href='tg://user?id={replied_user.id}'>{replied_user_name}</a>, {roast}"
        bot.send_message(message.chat.id, response, parse_mode="HTML")
        log_to_owner(message.from_user, command, response)

    # If the user mentions someone with @username
    elif '@' in command:
        username = command.split('@')[1].strip()
        roast = generate_roast(username)
        response = f"Hey @{username}, {roast}"
        bot.send_message(message.chat.id, response, parse_mode="HTML")
        log_to_owner(message.from_user, command, response)

    # If the user types /roast without replying or mentioning
    else:
        roast = generate_roast(user_first_name)
        response = f"Hey <a href='tg://user?id={user_id}'>{user_first_name}</a>, {roast}"
        bot.send_message(message.chat.id, response, parse_mode="HTML")
        log_to_owner(message.from_user, command, response)

# Start polling the bot
bot.polling()
