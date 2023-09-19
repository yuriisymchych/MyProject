import telebot
from MyProject.modules.weather_module import fetch_weather
from MyProject.modules.exchange_rate_module import fetch_exchange_rates
from MyProject.modules.crypto_rate_module import fetch_crypto_rates
from MyProject.modules.donation_module import show_donation_menu, show_fund1_link, show_fund2_link, show_fund3_link


bot = telebot.TeleBot("6473924532:AAEuhs_ohhN1N17jixwPq4j55iVJl9Ga-qI")

user_states = {}

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    weather_button = telebot.types.KeyboardButton("Погода")
    exchange_rate_button = telebot.types.KeyboardButton("Курс валют")
    crypto_rate_button = telebot.types.KeyboardButton("Курс криптовалют")
    donate_button = telebot.types.KeyboardButton("Донат")
    markup.row(weather_button, exchange_rate_button)
    markup.row(crypto_rate_button)
    markup.row(donate_button)
    bot.reply_to(message, "Вітаю! Оберіть, яку інформацію ви хочете отримати:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Погода")
def get_weather(message):
    bot.reply_to(message, "Введіть назву міста, щоб дізнатися погоду.")
    bot.register_next_step_handler(message, process_city_step)

def process_city_step(message):
    try:
        city_name = message.text
        weather_data = fetch_weather(city_name)
        if weather_data:
            bot.send_message(message.chat.id, weather_data)
        else:
            bot.send_message(message.chat.id, "Не вдалося отримати погоду для цього міста.")
    except Exception as e:
        bot.send_message(message.chat.id, "Виникла помилка. Спробуйте ще раз пізніше.")

@bot.message_handler(func=lambda message: message.text == "Курс валют")
def get_exchange_rate(message):
    try:
        exchange_message = fetch_exchange_rates()
        bot.reply_to(message, exchange_message)
    except Exception as e:
        bot.reply_to(message, "Виникла помилка. Спробуйте ще раз пізніше.")


@bot.message_handler(func=lambda message: message.text == "Курс криптовалют")
def get_crypto_rate(message):
    try:
        crypto_message = fetch_crypto_rates()
        bot.reply_to(message, crypto_message)
    except Exception as e:
        bot.reply_to(message, "Виникла помилка. Спробуйте ще раз пізніше.")


@bot.message_handler(func=lambda message: message.text == "Донат")
def donate(message):
    show_donation_menu(bot, message, user_states)

    @bot.message_handler(func=lambda message: message.text == "Назад")
    def back_to_main_menu(message):
        if message.chat.id in user_states and user_states[message.chat.id] == "donate_menu":
            del user_states[message.chat.id]
            send_welcome(message)


@bot.message_handler(func=lambda message: message.text == "Фонд Сергія Притули")
def fund1_link(message):
    show_fund1_link(bot, message)

@bot.message_handler(func=lambda message: message.text == "Фонд 'Повернися живим'")
def fund2_link(message):
    show_fund2_link(bot, message)

@bot.message_handler(func=lambda message: message.text == "Фонд 'United24'")
def fund3_link(message):
    show_fund3_link(bot, message)

if __name__ == "__main__":
    bot.polling()
