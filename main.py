'''
This is the Main Class Which will be used to execute the function calls for functions we declare in other modules.

'''
# This is the updater class which is used to continously fetch
# updates from telegram.

from telegram.ext import Updater
updater = Updater(token='TOKEN', use_context=True)
import logging
from telegram import Update
from telegram.ext import CallbackContext




class Main:
    # This is the logging module that is used to log errors that happen when using 
    # the telegram API
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
    # This is a local instance of the dispatcher class
    dispatcher = updater.dispatcher
    def start(update: Update, context: CallbackContext):
        context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

    
