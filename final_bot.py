import os
from dotenv import load_dotenv
from dbhelper import DBHelper 
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, Bot
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    CallbackContext,
    MessageHandler,
    Filters,
)
from view_functions import *
from profile_functions import *

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

load_dotenv("./.env")
TOKEN = os.getenv("token")
bot = Bot(TOKEN)

db = DBHelper()

### START FUNCTIONS ###
def start(update: Update, context: CallbackContext):
    """To start the bot"""

    update.message.reply_text("Hello! This bot will help you engage potential recruiters.")
    update.message.reply_text("For recruiters, click /view" + "\nFor applicants, click /profile")

### FOR END FUNCTION ###
# Returns `ConversationHandler.END`, which tells the ConversationHandler that the conversation is over 
def end(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="See you next time!")
    return ConversationHandler.END
###

def error(update: Update, context: CallbackContext):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def exit_convo(update: Update, context: CallbackContext):
    update.message.reply_text("See you next time!")
    return ConversationHandler.END

### FOR MAIN FUNCTION TO RUN THE BOT###
def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    start_point = CommandHandler('start', start)

    applicant_convo = ConversationHandler(
        entry_points=[CommandHandler('profile', profile)], #profile function 
        states={
            "CREATE_PROFILE": [
                CommandHandler("exit", exit_convo),
                MessageHandler(Filters.text, create_profile)
            ],
            "ADD_PHONE": [
                CommandHandler("exit", exit_convo),
                MessageHandler(Filters.text, add_phone)
            ],
            "ADD_EMAIL": [
                CommandHandler("exit", exit_convo),
                MessageHandler(Filters.text, add_email)
            ],
            "MAIN_MENU": [
                CallbackQueryHandler(particulars, pattern='PARTICULARS'), #regular expression
                CallbackQueryHandler(links, pattern='LINKS'),
                CallbackQueryHandler(qna, pattern='QNA'),
                CallbackQueryHandler(end, pattern='QUIT'),
                
            ],
            "PARTICULARS_MENU": [
                CallbackQueryHandler(main_menu, pattern='BACK'),
                CallbackQueryHandler(end, pattern='QUIT'),
                CallbackQueryHandler(edit_name, pattern='EDIT_NAME'),
                CallbackQueryHandler(edit_mobile, pattern='EDIT_NUMBER'),
                CallbackQueryHandler(edit_email, pattern='EDIT_EMAIL'),
            ],
            "EDIT_NAME":[
                MessageHandler(Filters.text & ~Filters.command, save_name),
                CallbackQueryHandler(particulars, pattern='PARTICULARS'),
            ],
            "EDIT_MOBILE":[
                MessageHandler(Filters.text & ~Filters.command, save_mobile),
                CallbackQueryHandler(particulars, pattern='PARTICULARS'),
            ],
            "EDIT_EMAIL":[
                MessageHandler(Filters.text & ~Filters.command, save_email),
                CallbackQueryHandler(particulars, pattern='PARTICULARS'),
            ],
            "LINKS_MENU": [
                CallbackQueryHandler(main_menu, pattern='BACK'),
                CallbackQueryHandler(end, pattern='QUIT'),
                CallbackQueryHandler(edit_link, pattern='^LINK_'), #any button with starts LINK_ will call this function editlink 
                CallbackQueryHandler(new_link, pattern='NEWLINK'),
            ],
            "ADD_LINK_DESC":[
                MessageHandler(Filters.text & ~Filters.command, add_link_desc),
                CallbackQueryHandler(links, pattern='LINKS'),
            ],
            "ADD_LINK_URL":[
                MessageHandler(Filters.text & ~Filters.command, add_link_url),
                CallbackQueryHandler(links, pattern='LINKS'),
            ],
            "EDIT_LINK_DESC":[
                CommandHandler("next", edit_link_desc),
                MessageHandler(Filters.text & ~Filters.command, edit_link_desc),
                CallbackQueryHandler(links, pattern='LINKS')
            ],
            "EDIT_LINK_URL":[
                MessageHandler(Filters.text & ~Filters.command, edit_link_url),
                CallbackQueryHandler(links, pattern='LINKS'),
            ],
            "QNA_MENU": [
                CallbackQueryHandler(main_menu, pattern='BACK'),
                CallbackQueryHandler(end, pattern='QUIT'), 
                CallbackQueryHandler(edit_answer, pattern='^qna_'),
            ],
            "EDIT_ANSWER":[
                MessageHandler(Filters.text & ~Filters.command, user_answer),
                CallbackQueryHandler(qna, pattern='QNA')
            ],
        },
        fallbacks=[CommandHandler('exit', exit_convo)]
    )
    
    recruiter_convo = ConversationHandler(
        entry_points=[CommandHandler('view', view)],
        states = {
            "USERNAME": [
                CommandHandler('exit', exit_convo),
                MessageHandler(Filters.text, view_user_menu)
            ],
            "DISPLAY": [
                CallbackQueryHandler(end, pattern ="end"),
                CallbackQueryHandler(view_user_particulars, pattern ="view_particulars"),
                CallbackQueryHandler(view_user_links, pattern ="view_links"),
                CallbackQueryHandler(view_user_qna, pattern ="view_qna")
            ]

        },
        fallbacks = [CommandHandler('exit', exit_convo)]
    )

    # Add ConversationHandler to dispatcher that will be used for handling updates
    dispatcher.add_handler(start_point)
    dispatcher.add_handler(applicant_convo)
    dispatcher.add_handler(recruiter_convo)
    dispatcher.add_error_handler(error)


    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
