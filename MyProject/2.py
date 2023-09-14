import telebot
import requests


bot = telebot.TeleBot('6520371815:AAFTMm4xiqNz0wS8BKdidPfI-cyl5z7NJKs')

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

def fetch_weather(city_name):
    try:

        weather_api_key = '7e9e07edd2b4ea5f735de7b44ed7900d'
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={weather_api_key}&units=metric"
        response = requests.get(weather_url)
        data = response.json()

        if response.status_code == 200:
            weather_description = data['weather'][0]['description']
            temperature = data['main']['temp']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']

            weather_message = f"Погода в {city_name}:\n"
            weather_message += f"Стан погоди: {weather_description}\n"
            weather_message += f"Температура: {temperature}°C\n"
            weather_message += f"Вологість: {humidity}%\n"
            weather_message += f"Швидкість вітру: {wind_speed} м/с"

            return weather_message
        else:
            return None
    except Exception as e:
        return None

@bot.message_handler(func=lambda message: message.text == "Курс валют")
def get_exchange_rate(message):
    try:
        exchange_url = "https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5"
        response = requests.get(exchange_url)
        data = response.json()

        if response.status_code == 200:
            exchange_message = "Курс валют до гривні:\n"
            for currency in data:
                exchange_message += f"{currency['ccy']} -> {currency['base_ccy']}: {currency['buy']} - {currency['sale']}\n"
            bot.reply_to(message, exchange_message)
        else:
            bot.reply_to(message, "Не вдалося отримати курс валют.")
    except Exception as e:
        bot.reply_to(message, "Виникла помилка. Спробуйте ще раз пізніше.")

@bot.message_handler(func=lambda message: message.text == "Курс криптовалют")
def get_crypto_rate(message):
    try:
        crypto_currencies = ['bitcoin', 'ethereum', 'binancecoin', 'cardano', 'ripple']
        crypto_message = "Курс криптовалют на даний час:\n"

        for crypto in crypto_currencies:
            crypto_url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto}&vs_currencies=usd"
            response = requests.get(crypto_url)
            data = response.json()

            if response.status_code == 200:
                price = data[crypto]['usd']
                crypto_message += f"{crypto.capitalize()}: ${price}\n"
            else:
                crypto_message += f"{crypto.capitalize()}: Немає даних\n"

        bot.reply_to(message, crypto_message)
    except Exception as e:
        bot.reply_to(message, "Виникла помилка. Спробуйте ще раз пізніше.")


@bot.message_handler(func=lambda message: message.text == "Донат")
def donate(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    fund1_button = telebot.types.KeyboardButton("Фонд Сергія Притули")
    fund2_button = telebot.types.KeyboardButton("Фонд 'Повернися живим'")
    fund3_button = telebot.types.KeyboardButton("Фонд 'United24'")
    back_button = telebot.types.KeyboardButton("Назад")

    markup.row(fund1_button)
    markup.row(fund2_button)
    markup.row(fund3_button)
    markup.row(back_button)

    bot.reply_to(message, "Оберіть фонд, на який ви бажаєте здійснити донат:", reply_markup=markup)

    user_states[message.chat.id] = "donate_menu"

    @bot.message_handler(func=lambda message: message.text == "Назад")
    def back_to_main_menu(message):
        if message.chat.id in user_states and user_states[message.chat.id] == "donate_menu":

            del user_states[message.chat.id]
            send_welcome(message)


@bot.message_handler(func=lambda message: message.text == "Фонд Сергія Притули")
def fund1_link(message):
    bot.reply_to(message, "Сайт Фонду Сергія Притули: [https://prytulafoundation.org/]")


@bot.message_handler(func=lambda message: message.text == "Фонд 'Повернися живим'")
def fund2_link(message):
    bot.reply_to(message, "Сайт Фонду 'Повернися живим': [https://savelife.in.ua/]")


@bot.message_handler(func=lambda message: message.text == "Фонд 'United24'")
def fund3_link(message):
    bot.reply_to(message, "Сайт Фонду 'United24': [https://u24.gov.ua/]")

if __name__ == "__main__":
    bot.polling()
