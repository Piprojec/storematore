import os
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

bot_token = os.getenv('BOT_TOKEN')  # Получаем токен бота из переменных окружения

bot = Bot(token=bot_token)
updater = Updater(bot=bot)
dispatcher = updater.dispatcher

phone_catalog = [
    {'id': 1, 'name': 'iPhone X', 'price': '1000$'},
    {'id': 2, 'name': 'Samsung Galaxy S10', 'price': '900$'},
    {'id': 3, 'name': 'Google Pixel 3', 'price': '800$'}
]


def start(update: Update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Я бот Телеграф. Чем могу помочь?")


def catalog(update: Update, context):
    catalog_text = "Каталог продажи телефонов:\n\n"
    for phone in phone_catalog:
        catalog_text += f"{phone['id']}. {phone['name']} - {phone['price']}\n"
    context.bot.send_message(chat_id=update.effective_chat.id, text=catalog_text)


def order(update: Update, context):
    if len(context.args) == 0:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Пожалуйста, укажите номер телефона из каталога.")
    else:
        phone_id = int(context.args[0])
        phone = next((p for p in phone_catalog if p['id'] == phone_id), None)
        if phone:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"Заказ на телефон {phone['name']} размещен.")
        else:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="Неправильный номер телефона.")


def echo(update: Update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Извините, я не понимаю такую команду.")


start_handler = CommandHandler('start', start)
catalog_handler = CommandHandler('catalog', catalog)
order_handler = CommandHandler('order', order)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(catalog_handler)
dispatcher.add_handler(order_handler)
dispatcher.add_handler(MessageHandler(Filters.text, echo))

updater.start_polling()
