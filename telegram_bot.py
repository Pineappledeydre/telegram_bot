import telebot

# Токен от BotFather
API_TOKEN = "7035407255:AAH8uX3eMjYhSipe09cYHDcMV5Wp-mbeBuA"

# Создание объекта бота
bot = telebot.TeleBot(API_TOKEN)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message,
        "Привет, я бот! Я умею искать информацию в интернете за тебя. Напиши свой запрос в сообщении ниже."
    )

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_query(message):
    user_query = message.text  # Текст сообщения от пользователя
    google_search_link = f"https://google.com/?q={'+'.join(user_query.split())}"  # Генерация ссылки
    bot.reply_to(message, f"Вот что я нашел: {google_search_link}")  # Ответ пользователю

if __name__ == "__main__":
    print("Бот запущен и работает...")
    bot.polling(none_stop=True)

