import json
import requests
import logging
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
import os
from dbhelper2 import DBHelper 

<<<<<<< Updated upstream


=======
>>>>>>> Stashed changes
TOKEN = '5093335972:AAF5XKRoWd9AEVycikG7CzPljBo8RpKqBtE'
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
CREATEPROFILE, ADDPHONE, EXISTING = range(3)


db = DBHelper()


def start(update: Update, context: CallbackContext) -> int:
    """To start the bot"""

    update.message.reply_text("Hello! This bot will help you engage potential recruiters.\n" +
    "First, let's check if you already have a resume with us.")
    username = update.message.chat.username

    # check if the user's username can currently be found inside the database
    fullname = db.get_fullname(username)
    
    if fullname == None:
        update.message.reply_text("Looks like you don't currently have a resume with us.\n" +
        "Let's get started on that!"
        )
        update.message.reply_text("What is your fullname?", reply_markup=ReplyKeyboardRemove())
        return CREATEPROFILE

    else:
        reply_keyboard = [['View My Resume', 'Edit My Resume']]
        update.message.reply_text("Welcome back " + fullname + "!\n" +
        "Would you like to view your resume or edit your resume?\n\n",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        )
        return EXISTING

        
def createprofile(update: Update, context: CallbackContext) -> int:
    fullname = update.message.text
    update.message.reply_text("Great " + fullname + ", we've added to our database.")
    db.create_fullname(update.message.chat.username, fullname)
    update.message.reply_text("Next, add your phone number or press /skip for now")
    return ADDPHONE

def addphone(update: Update, context: CallbackContext) -> int:
    phone = update.message.text
    update.message.reply_text("Great, let's add your contact number.")
    db.add_phone(update.message.chat.username, phone)
    reply_keyboard = [['View My Resume', 'Edit My Resume']]
    update.message.reply_text("We're all done setting up your profile.\n" +
    "Would you like to view your resume or edit your resume?",
    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return EXISTING

def skipphone(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("No worries, you can always add your contact number another time.")
    reply_keyboard = [['View My Resume', 'Edit My Resume']]
    update.message.reply_text("We're all done setting up your profile.\n" +
    "Would you like to view your resume or edit your resume?",
    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return EXISTING


def viewresume(update:Update, context: CallbackContext) -> int:
    username = update.message.chat.username
    retrieveprofile = db.get_profile(username)[0]
    name = retrieveprofile['fullname']
    contact = retrieveprofile['contact_no']
    email = retrieveprofile['email']
    update.message.reply_text("Testing...")
    update.message.reply_text(name)

    # return (name, contact,email)

def error(update: Update, context: CallbackContext):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    """Start the bot"""
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    conv_handler = ConversationHandler (
        entry_points = [CommandHandler('start', start)],
        states = {
            CREATEPROFILE: [MessageHandler(Filters.text, createprofile)],
            ADDPHONE: [MessageHandler(Filters.text, addphone)],
            EXISTING: [MessageHandler(Filters.text, deciding)]
        },
        fallbacks = [CommandHandler('start', start)]
    )
    dp.add_handler(conv_handler)
    dp.add_error_handler(error)
    # dp.add_handler(MessageHandler(Filters.text, add_item))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

