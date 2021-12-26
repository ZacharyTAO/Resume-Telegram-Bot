from typing import Callable
import test_bot_apikey as key
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    CallbackContext,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# Stages
FIRST, SECOND, THIRD= range(3)
# Callback data
ONE, TWO, THREE, FOUR , FIVE, SIX, SEVEN, EIGHT, NINE, TEN, Q1, Q2, Q3, Q4= range(14)

def edit(update: Update, context: CallbackContext) -> int:
    """Send message on `/start`."""
    # Get user that sent /start and log his name
    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)
    keyboard = [
        [
            InlineKeyboardButton("Particulars", callback_data=str(ONE)),
            InlineKeyboardButton("Links", callback_data=str(TWO)),
        ],
        [
            InlineKeyboardButton("Q&A", callback_data=str(THREE)),
            InlineKeyboardButton("Confirmation Menu", callback_data=str(FOUR)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    update.message.reply_text("Main Menu", reply_markup=reply_markup)
    # Tell ConversationHandler that we're in state `FIRST` now
    return FIRST

def particulars(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Confirmation Menu", callback_data=str(FOUR)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Once you are done editing, click on 'confirmation menu'", reply_markup=reply_markup
    )
    return FIRST


def links(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Confirmation Menu", callback_data=str(FOUR)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Once you are done editing, click on 'confirmation menu'", reply_markup=reply_markup
    )
    return FIRST

def qna(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Edit Answers", callback_data=str(SEVEN)),
        ],
        [
            InlineKeyboardButton("Confirmation Menu", callback_data=str(FOUR)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text=
        "1. Describe yourself\n\n"+ 

        "2. Why are you applying for this job?\n\n"+ 

        "3. What are some of your strengths and weaknesses?\n\n"+

        "4. What are some challenges you have experienced and how did you overcome it?\n\n"+ 
        
        "Question 1 answer\n\n"+

        "Question 2 answer\n\n"+
        
        "Question 3 answer\n\n"+

        "Question 4 answer\n\n"

        , reply_markup=reply_markup)
 
    reply_markup = InlineKeyboardMarkup(keyboard)
    return FIRST

def question_menu(update: Update, context: CallbackContext) -> int:
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
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="select a question", reply_markup=reply_markup
    )
    return THIRD

def question1(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Confirmation Menu", callback_data=str(FOUR)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Input answer for question 1. \n\n Press enter to confirm answer. \n\n Click on 'confirmation menu' to go back or end.\n\n", reply_markup=reply_markup
    )
    return FIRST

def question2(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Confirmation Menu", callback_data=str(FOUR)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Input answer for question 1. \n\n Press enter to confirm answer. \n\n Click on 'confirmation menu' to go back or end.\n\n",reply_markup=reply_markup
    )
    return FIRST

def question3(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="q3")
    return THIRD

def question4(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="q4")
    return THIRD

def confirmation_menu(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Back", callback_data=str(FIVE)),
            InlineKeyboardButton("Done", callback_data=str(SIX)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="To go back to the main menu, press 'back' or else press 'done' to end", reply_markup=reply_markup
    )
    return SECOND

def back(update: Update, context: CallbackContext) -> int:
    """Prompt same text & keyboard as `start` does but not as new message"""
    # Get CallbackQuery from Update
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Particulars", callback_data=str(ONE)),
            InlineKeyboardButton("Links", callback_data=str(TWO)),
        ],
        [
            InlineKeyboardButton("Q&A", callback_data=str(THREE)),
            InlineKeyboardButton("Confirmation Menu", callback_data=str(FOUR)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    query.edit_message_text(text="Main Menu", reply_markup=reply_markup)
    return FIRST

def done(update: Update, context: CallbackContext) -> int:
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over.
    """
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="See you next time!")
    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(key.API_KEY)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', edit)],
        states={
            FIRST: [
                CallbackQueryHandler(particulars, pattern='^' + str(ONE) + '$'),
                CallbackQueryHandler(links, pattern='^' + str(TWO) + '$'),
                CallbackQueryHandler(qna, pattern='^' + str(THREE) + '$'),
                CallbackQueryHandler(question_menu, pattern='^' + str(SEVEN) + '$'),
                CallbackQueryHandler(confirmation_menu, pattern='^' + str(FOUR) + '$'),
            ],
            SECOND: [
                CallbackQueryHandler(back, pattern='^' + str(FIVE) + '$'),
                CallbackQueryHandler(done, pattern='^' + str(SIX) + '$'),  
            ],
            THIRD: [
                CallbackQueryHandler(question1, pattern='^' + str(Q1) + '$'),
                CallbackQueryHandler(question2, pattern='^' + str(Q2) + '$'),
                CallbackQueryHandler(question2, pattern='^' + str(Q3) + '$'), 
                CallbackQueryHandler(question2, pattern='^' + str(Q4) + '$'),  
            ]
        },
        fallbacks=[CommandHandler('start', edit)],
    )

    # Add ConversationHandler to dispatcher that will be used for handling updates
    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()