import os
import telebot
from flask import Flask, request
import logging
import random

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Telegram API Token and Webhook URL
API_TOKEN = "7451259345:AAGAXrbm7xanA5ef6HfLqdl51qnI6xopNLA"  # Your bot token
WEBHOOK_URL = "https://telegram-bot-pineappledeydre.onrender.com"  # Your webhook URL

# Create bot and Flask app
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# Handler for /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    logger.info(f"Received /start command from user {message.chat.id}")
    bot.reply_to(message, "Привет, я бот! Я умею искать информацию в интернете за тебя.")

# Handler for /help command
@bot.message_handler(commands=['help'])
def send_help(message):
    logger.info(f"Received /help command from user {message.chat.id}")
    bot.reply_to(
        message,
        "Напишите запрос, и я найду ссылку в Google. Напишите 'шутка', чтобы услышать смешное!"
    )

# Handler for "шутка"
@bot.message_handler(func=lambda message: message.text.lower() == "шутка")
def send_joke(message):
    jokes = [
        "Почему программисты не любят природу? Слишком много багов.",
        "Что делает программист, когда ему скучно? Зависает.",
        "Какая самая страшная ошибка у программистов? Ошибка 404: шутка не найдена.",
    ]
    joke = random.choice(jokes)
    logger.info(f"Sending joke to user {message.chat.id}: {joke}")
    bot.reply_to(message, joke)

# Handler for general text messages
@bot.message_handler(func=lambda message: True)
def handle_query(message):
    user_query = message.text
    google_search_link = f"https://google.com/?q={'+'.join(user_query.split())}"
    logger.info(f"Received query from user {message.chat.id}: {user_query}")
    bot.reply_to(message, f"Вот что я нашел: {google_search_link}")

# Webhook route to receive updates from Telegram (fixed route)
@app.route('/webhook', methods=['POST'])
def webhook():
    logger.info("Received POST request to webhook.")
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '!', 200

# Route to confirm the bot is running
@app.route('/')
def index():
    logger.info("Index route accessed.")
    return 'Bot is running!', 200

if __name__ == "__main__":
    try:
        bot.remove_webhook()
        bot.set_webhook(url=f"{WEBHOOK_URL}/webhook")  # Use /webhook route
        logger.info(f"Webhook set to: {WEBHOOK_URL}/webhook")
    except Exception as e:
        logger.error(f"Error setting webhook: {e}")

    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)
