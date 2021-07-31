from telegram import Update 
from telegram.ext import Updater, CommandHandler, CallbackContext, Filters
import time 
import sqlite3

from telegram.utils.helpers import create_deep_linked_url
from lib.users import User


TOKEN = "1930371596:AAGBrUire3YxhDeA4so2GmBL5x2YypYNjTc"

def get(update: Update, context: CallbackContext):
    print(update.message.from_user.username)


def error(bot, update, error):
    print("error")

updater = Updater(TOKEN)
updater.dispatcher.add_handler(CommandHandler('get',get))

updater.dispatcher.logger.addFilter((lambda s: not s.msg.endswith('A TelegramError was raised while processing the Update')))
updater.dispatcher.add_error_handler(error)

updater.start_polling()
updater.idle()