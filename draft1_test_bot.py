from typing import Callable
from tele_bot_main_dbhelper import DBHelper 
import test_bot_apikey as key
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    CallbackContext,
    MessageHandler,
    Filters,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# Stages
CREATEPROFILE, ADDPHONE, MESSAGE, FIRST, SECOND, THIRD, FOURTH= range(7)
# Callback data
PARTICULARS, LINKS, QNA, FOUR , BACK, QUIT, NAME, MOBILENUMBER, EMAIL, LINK1, LINK2, LINK3, LINK4, Q1, Q2, Q3, Q4= range(17)

### calling dbhelper stepbro for help ###

db = DBHelper()

### START FUNCTIONS ###
def start(update: Update, context: CallbackContext) -> int:
    """To start the bot"""

    update.message.reply_text("Hello! This bot will help you engage potential recruiters.")
    username = update.message.chat.username

    # check if the user's username can currently be found inside the database
    fullname = db.get_fullname(username)
    
    if fullname == None:
        update.message.reply_text("Looks like you don't currently have a profile with us.\n\n" +
        "Let's get started on that!"
        )
        update.message.reply_text("What is your fullname?", reply_markup=ReplyKeyboardRemove())
        return CREATEPROFILE

    else:
        update.message.reply_text("Welcome back " + fullname + "!\n" +
        "Type /edit to edit your resume\n\n")
        
def createprofile(update: Update, context: CallbackContext) -> int:
    fullname = update.message.text
    update.message.reply_text("Great " + fullname + ", we've added to our database.")
    db.create_fullname(update.message.chat.username, fullname)
    update.message.reply_text("Next, add your phone number")
    return ADDPHONE

def addphone(update: Update, context: CallbackContext) -> int:
    phone = update.message.text
    db.add_phone(update.message.chat.username, phone)
    update.message.reply_text("We're all done setting up your profile.\n" + "Type /edit and press enter to view and edit your profile")
    return ConversationHandler.END
###

### FOR MAIN MENU FUNCTIONS ###
def main_menu(update: Update, context: CallbackContext) -> int:
    """Send message on `/start`."""
    # Get user that sent /start and log his name
    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)
    keyboard = [
        [
            InlineKeyboardButton("Particulars", callback_data=str(PARTICULARS)),
            InlineKeyboardButton("Links", callback_data=str(LINKS)),
        ],
        [
            InlineKeyboardButton("Q&A", callback_data=str(QNA)),
            InlineKeyboardButton("End", callback_data=str(QUIT)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    update.message.reply_text("Main Menu", reply_markup=reply_markup)
    # Tell ConversationHandler that we're in state `FIRST` now
    return FIRST

# because main menu function is not defined in first state, we use this instead to refer back to main menu
def back_main_menu(update: Update, context: CallbackContext) -> int:
    """Prompt same text & keyboard as `start` does but not as new message"""
    # Get CallbackQuery from Update
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Particulars", callback_data=str(PARTICULARS)),
            InlineKeyboardButton("Links", callback_data=str(LINKS)),
        ],
        [
            InlineKeyboardButton("Q&A", callback_data=str(QNA)),
            InlineKeyboardButton("End", callback_data=str(QUIT)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    query.edit_message_text(text="Main Menu", reply_markup=reply_markup)
    return FIRST
###

### FOR END FUNCTION ###
# Returns `ConversationHandler.END`, which tells the ConversationHandler that the conversation is over 
def end(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="See you next time!")
    return ConversationHandler.END
###

###
def particulars(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Name", callback_data=str(NAME)),
            InlineKeyboardButton("Mobile Number", callback_data=str(MOBILENUMBER)),
            InlineKeyboardButton("Email", callback_data=(EMAIL))
        ],
        [
            InlineKeyboardButton("Back", callback_data=str(BACK)),
            InlineKeyboardButton("End", callback_data=str(QUIT)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Particulars Menu", reply_markup=reply_markup
    )
# goes to second state
    return SECOND

def name(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Back", callback_data=str(PARTICULARS)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Type in your name and press enter", reply_markup=reply_markup
    )
    return SECOND

def mobilenumber(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Back", callback_data=str(PARTICULARS)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Type in your mobile number and press enter", reply_markup=reply_markup
    )
    return SECOND

def email(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Back", callback_data=str(PARTICULARS)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Type in your eamail and press enter", reply_markup=reply_markup
    )
    return SECOND
###

### FOR LINK FUNCTIONS ###
def links(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Link 1", callback_data=str(LINK1)),
            InlineKeyboardButton("Link 2", callback_data=str(LINK2)),
        ],
        [
            InlineKeyboardButton("Link 3", callback_data=str(LINK3)),
            InlineKeyboardButton("Link 4", callback_data=str(LINK4)),
        ],
        [
            InlineKeyboardButton("Back", callback_data=str(BACK)),
            InlineKeyboardButton("End", callback_data=str(QUIT)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Link Menu", reply_markup=reply_markup
    )
    # goes to third state
    return THIRD

def link1(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Back", callback_data=str(LINKS)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Input name for your link and the URL", reply_markup=reply_markup
    )
    return THIRD

def link2(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Back", callback_data=str(LINKS)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Input name for your link and the URL", reply_markup=reply_markup
    )
    return THIRD

def link3(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Back", callback_data=str(LINKS)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Input name for your link and the URL", reply_markup=reply_markup
    )
    return THIRD

def link4(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Back", callback_data=str(LINKS)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Input name for your link and the URL", reply_markup=reply_markup
    )
    return THIRD
###

### FOR QNA FUNCTIONS ###
def qna(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Q1", callback_data=str(Q1)),
            InlineKeyboardButton("Q2", callback_data=str(Q2)),
        ],
        [
            InlineKeyboardButton("Q3", callback_data=str(Q3)),
            InlineKeyboardButton("Q4", callback_data=str(Q4)),
        ],
        [
            InlineKeyboardButton("Back", callback_data=str(BACK)),
            InlineKeyboardButton("End", callback_data=str(QUIT)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text=
        "Question & Answer Menu"+

        "1. Describe yourself\n\n"+ 

        "Question 1 answer\n\n"+

        "2. Why are you applying for this job?\n\n"+ 

        "Question 2 answer\n\n"+

        "3. What are some of your strengths and weaknesses?\n\n"+

        "Question 3 answer\n\n"+

        "4. What are some challenges you have experienced and how did you overcome it?\n\n"+ 

        "Question 4 answer\n\n"

        , reply_markup=reply_markup)
 
    reply_markup = InlineKeyboardMarkup(keyboard)
    # goes to fourth state
    return FOURTH

def question1(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Back", callback_data=str(QNA)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text=
        "1. Describe yourself\n\n" + 
        "Type in an answer for question 1. \n\n" + 
        "Press enter to confirm answer. \n\n" + 
        "Click on 'back' to return to question menu.\n\n", reply_markup=reply_markup
    )
    return FOURTH

def question2(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Back", callback_data=str(QNA)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text=
        "2. Why are you applying for this job?\n\n"+ 
        "Type in an answer for question 1. \n\n" + 
        "Press enter to confirm answer. \n\n" + 
        "Click on 'back' to return to question menu.\n\n", reply_markup=reply_markup
    )
    return FOURTH

def question3(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Back", callback_data=str(QNA)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text=
        "3. What are some of your strengths and weaknesses?\n\n"+
        "Type in an answer for question 1. \n\n" + 
        "Press enter to confirm answer. \n\n" + 
        "Click on 'back' to return to question menu.\n\n", reply_markup=reply_markup
    )
    return FOURTH

def question4(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Back", callback_data=str(QNA)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text=
        "4. What are some challenges you have experienced and how did you overcome it?\n\n"+ 
        "Type in an answer for question 1. \n\n" + 
        "Press enter to confirm answer. \n\n" + 
        "Click on 'back' to return to question menu.\n\n", reply_markup=reply_markup
    )
    return FOURTH
###

### FOR MAIN FUNCTION TO RUN THE BOT###
def main() -> None:
    updater = Updater(key.API_KEY)
    dispatcher = updater.dispatcher

    conv_handler1 = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CREATEPROFILE: [MessageHandler(Filters.text, createprofile)],
            ADDPHONE: [MessageHandler(Filters.text, addphone)],
        },
        fallbacks=[CommandHandler('start', start)]
    )

    conv_handler2 = ConversationHandler(
        entry_points=[CommandHandler('edit', main_menu)],
        states={
            FIRST: [
                CallbackQueryHandler(particulars, pattern='^' + str(PARTICULARS) + '$'),
                CallbackQueryHandler(links, pattern='^' + str(LINKS) + '$'),
                CallbackQueryHandler(qna, pattern='^' + str(QNA) + '$'),
                CallbackQueryHandler(back_main_menu, pattern='^' + str(BACK) + '$'),
                CallbackQueryHandler(end, pattern='^' + str(QUIT) + '$'),
                
            ],
            SECOND: [
                CallbackQueryHandler(particulars, pattern='^' + str(PARTICULARS) + '$'),
                CallbackQueryHandler(back_main_menu, pattern='^' + str(BACK) + '$'),
                CallbackQueryHandler(end, pattern='^' + str(QUIT) + '$'),
                CallbackQueryHandler(name, pattern='^' + str(NAME) + '$'),
                CallbackQueryHandler(mobilenumber, pattern='^' + str(MOBILENUMBER) + '$'),
                CallbackQueryHandler(email, pattern='^' + str(EMAIL) + '$'),
            ],
            THIRD: [
                CallbackQueryHandler(links, pattern='^' + str(LINKS) + '$'),
                CallbackQueryHandler(back_main_menu, pattern='^' + str(BACK) + '$'),
                CallbackQueryHandler(end, pattern='^' + str(QUIT) + '$'),
                CallbackQueryHandler(link1, pattern='^' + str(LINK1) + '$'), 
                CallbackQueryHandler(link2, pattern='^' + str(LINK2) + '$'), 
                CallbackQueryHandler(link3, pattern='^' + str(LINK3) + '$'), 
                CallbackQueryHandler(link4, pattern='^' + str(LINK4) + '$'), 
            ],
            FOURTH: [
                CallbackQueryHandler(qna, pattern='^' + str(QNA) + '$'),
                CallbackQueryHandler(back_main_menu, pattern='^' + str(BACK) + '$'),
                CallbackQueryHandler(end, pattern='^' + str(QUIT) + '$'), 
                CallbackQueryHandler(question1, pattern='^' + str(Q1) + '$'),
                CallbackQueryHandler(question2, pattern='^' + str(Q2) + '$'),
                CallbackQueryHandler(question3, pattern='^' + str(Q3) + '$'), 
                CallbackQueryHandler(question4, pattern='^' + str(Q4) + '$'), 
            ],
        },
        fallbacks=[CommandHandler('edit', main_menu)],
    )

    # Add ConversationHandler to dispatcher that will be used for handling updates
    dispatcher.add_handler(conv_handler1)
    dispatcher.add_handler(conv_handler2)

    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()