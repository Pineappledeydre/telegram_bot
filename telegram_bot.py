import os
import telebot
from flask import Flask, request
import logging
import random

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Telegram API Token and Webhook URL
API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

if not API_TOKEN:
    raise ValueError("Telegram API token not found!")
if not WEBHOOK_URL:
    raise ValueError("Webhook URL not found!")

# Create bot and Flask app
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# Handler for /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    logger.info(f"Processing /start command from user {message.chat.id}")
    try:
        bot.reply_to(message, "Привет, я бот! Я умею искать информацию в интернете за тебя.")
        logger.info(f"Reply sent to user {message.chat.id}")
    except Exception as e:
        logger.error(f"Failed to send reply: {e}")

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
    user_query = message.text  # User's message text
    google_search_link = f"https://google.com/?q={'+'.join(user_query.split())}"  # Generate Google search link
    bot.reply_to(message, f"Вот что я нашел: {google_search_link}")  # Reply with the link
    logger.info(f"Processed query from user {message.chat.id}: {user_query}")

# Webhook route to receive updates from Telegram
@app.route('/' + API_TOKEN, methods=['POST'])
def webhook():
    logger.info("Received POST request to webhook.")
    try:
        json_string = request.get_data().decode('utf-8')
        logger.info(f"Request data: {json_string}")
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        logger.info("Processed new update.")
    except Exception as e:
        logger.error(f"Error processing update: {e}")
    return '!', 200

# Route to confirm the bot is running
@app.route('/')
def index():
    logger.info("Index route accessed.")
    return 'Bot is running!', 200

if __name__ == "__main__":
    # Remove existing webhook (if any) and set a new one
    bot.remove_webhook()
    bot.set_webhook(url=f"{WEBHOOK_URL}/{API_TOKEN}")
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
