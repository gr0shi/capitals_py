import telebot
import requests
import re
from bs4 import BeautifulSoup

# Токен бота
TOKEN = "***********YOUR_TOKEN***********"

# Создаем экземпляр бота
bot = telebot.TeleBot(TOKEN)


# Обработчик команды /start
@bot.message_handler(commands=["start"])
def send_welcome(message):
    # Отправляем приветственное сообщение пользователю
    bot.reply_to(
        message,
        f"Привет, {message.from_user.first_name}! Я бот, который может найти столицу любой страны. Напишите название страны, и я скажу вам какова ее столица! \n\nℹ️ Для информации вызовите /help",
    )


# Обработчик команды /help
@bot.message_handler(commands=["help"])
def send_help(message):
    # Отправляем сообщение с информацией о том, как пользоваться ботом
    bot.reply_to(
        message,
        "Чтобы узнать столицу какой-либо страны, отправьте мне название этой страны с большой буквы. \nЯ поддерживаю ввод как с кириллицы так и с латиницы.\n\n💡 Для использования бота, вызовите: /start \n🆗 Для проверки статуса бота вызовите: /status",
    )


# Обработчик команды /status
@bot.message_handler(commands=["status"])
def send_status(message):
    # Отправляем сообщение с информацией о статусе бота
    bot.reply_to(
        message,
        "🆗 Бот работает.\nЕсли на вызов фунции /status бот не реагирует, то скорее всего он сейчас отключен.",
    )


# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def send_capital(message):
    # Получаем название страны из текста сообщения
    country = message.text

    # Проверяем, что слово начинается с большой буквы
    if not country.istitle():
        bot.reply_to(message, "Название страны должно начинаться с большой буквы")
        return

    if re.match("^[a-zA-Z]+$", message.text):  # Ответ для латиницы
        # Формируем URL для запроса на сайт с информацией о стране
        url_en = f"https://en.wikipedia.org/wiki/{country}"

        # Отправляем GET запрос на сайт и получаем содержимое страницы
        response = requests.get(url_en)
        soup = BeautifulSoup(response.text, "html.parser")

        # Ищем таблицу с информацией о стране и находим в ней строку с названием столицы
        table_en = soup.find("th", scope="row", class_="infobox-label")
        if table_en is not None:
            capital_row = table_en.find_next_sibling("td")
            if capital_row is not None:
                capital = capital_row.find("a").text.strip()

                # Отправляем сообщение с названием столицы пользователю
                bot.reply_to(message, f"{country} ➡️ {capital}")
            else:
                bot.reply_to(
                    message, f"Не удалось найти информацию о столице {country}"
                )
        else:
            bot.reply_to(message, f"Не удалось найти информацию о стране {country}")

    else:  # Ответ для кириллицы
        # Формируем URL для запроса на сайт с информацией о стране
        url_ru = f"https://ru.wikipedia.org/wiki/{country}"

        # Отправляем GET запрос на сайт и получаем содержимое страницы
        response = requests.get(url_ru)
        soup = BeautifulSoup(response.text, "html.parser")

        # Ищем таблицу с информацией о стране и находим в ней строку с названием столицы
        table_ru = soup.find("tbody")
        if table_ru is not None:
            capital_row = table_ru.find("th", string="Столица")
            if capital_row is not None:
                capital = capital_row.find_next_sibling("td").text.strip()

                # Отправляем сообщение с названием столицы пользователю
                bot.reply_to(message, f"{country} ➡️ {capital}")
            else:
                bot.reply_to(
                    message, f"Не удалось найти информацию о столице {country}"
                )
        else:
            bot.reply_to(message, f"Не удалось найти информацию о стране {country}")


# Запускаем бота
bot.polling()
