import telebot

def show_donation_menu(bot, message, user_states):
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



def show_fund1_link(bot, message):
    bot.reply_to(message, "Сайт Фонду Сергія Притули: [https://prytulafoundation.org/]")

def show_fund2_link(bot, message):
    bot.reply_to(message, "Сайт Фонду 'Повернися живим': [https://savelife.in.ua/]")

def show_fund3_link(bot, message):
    bot.reply_to(message, "Сайт Фонду 'United24': [https://u24.gov.ua/]")
