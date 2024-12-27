import os
import telebot
from flask import Flask, request

# Telegram API Token from environment variable
API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # URL from environment variables, e.g., https://your-render-url.onrender.com

if not API_TOKEN:
    raise ValueError("Telegram API token not found! Ensure TELEGRAM_BOT_TOKEN is set as an environment variable.")
if not WEBHOOK_URL:
    raise ValueError("Webhook URL not found! Ensure WEBHOOK_URL is set as an environment variable.")

# Create bot object
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# Command handler for /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message,
        "Привет, я бот! Я умею искать информацию в интернете за тебя. Напиши свой запрос в сообщении ниже."
    )

# Webhook route to receive updates from Telegram
@app.route('/' + API_TOKEN, methods=['POST'])
def webhook():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '!', 200

# Route to confirm the bot is running
@app.route('/')
def index():
    return 'Bot is running!', 200

if __name__ == "__main__":
    # Remove existing webhook (if any) and set a new one
    bot.remove_webhook()
    bot.set_webhook(url=f"{WEBHOOK_URL}/{API_TOKEN}")
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
