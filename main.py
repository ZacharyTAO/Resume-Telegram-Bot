'''
This is the Main Class Which will be used to execute the function calls for functions we declare in other modules.

'''
# This is the updater class which is used to continously fetch
# updates from telegram.

import telegram
from telegram.ext import Updater

import logging
from pathlib import Path
from dotenv import load_dotenv
import os
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler


# Using an environment Path to store the token so that we do not cause errors pushing to git 
# due to exposing our api Keys.

env_path =  Path('.')/'.env'
load_dotenv(dotenv_path=env_path)
updater = Updater(token=os.environ['TOKEN'], use_context=True)



class Main:
    # This is the logging module that is used to log errors that happen when using 
    # the telegram API to ensure that the errors caused by the 
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
    # This is a local instance of the dispatcher class
    dispatcher = updater.dispatcher
    
    '''
    This is a CallBack Function that will get called when the /start command is initiated. The bot will first reply to the user
    with a welcome message and then give them an option to choose if they are an employer or an employee    
    '''   
    def start(update: Update, context: CallbackContext):
        # Sends the Welcome message to the user for using the bot.
        context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to Resume Hacker Bot " + "🖊")
        # Create an custom_keyboard that will allow the user to  choose between having an employee interface or an employer interface.
        custom_keyboard = [[telegram.keyboardbutton.KeyboardButton(text="I am an Employer")],[telegram.keyboardbutton.KeyboardButton(text="I am an Employee")]]
        custom_keyboard_markup= telegram.ReplyKeyboardMarkup(custom_keyboard)
        # Sends the Custom Keyboard options to the users to allow them to choose the option based on their needs.
        context.bot.send_message(chat_id=update.effective_chat.id,text ="Please Choose Your Option",reply_markup = custom_keyboard_markup)
    start_handler = CommandHandler('start', start)
    






if __name__ == '__main__':
    Main.dispatcher.add_handler(Main.start_handler)

    updater.start_polling()