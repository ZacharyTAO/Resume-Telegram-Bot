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
FIRST, SECOND = range(2)
# Callback data
ONE, TWO, THREE, FOUR = range(4)


def start(update: Update, context: CallbackContext) -> int:
    """Send message on `/start`."""
    # Get user that sent /start and log his name
    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)

    keyboard = [
        [
            InlineKeyboardButton("1", callback_data=str(ONE)),
            InlineKeyboardButton("2", callback_data=str(TWO)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    update.message.reply_text("Start handler, Choose a route", reply_markup=reply_markup)
    # Tell ConversationHandler that we're in state `FIRST` now
    return FIRST


def start_over(update: Update, context: CallbackContext) -> int:
    """Prompt same text & keyboard as `start` does but not as new message"""
    # Get CallbackQuery from Update
    query = update.callback_query

    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("1", callback_data=str(ONE)),
            InlineKeyboardButton("2", callback_data=str(TWO)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Instead of sending a new message, edit the message that
    # originated the CallbackQuery. This gives the feeling of an
    # interactive menu.
    query.edit_message_text(text="Start handler, Choose a route", reply_markup=reply_markup)
    return FIRST


def one(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("3", callback_data=str(THREE)),
            InlineKeyboardButton("4", callback_data=str(FOUR)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="First CallbackQueryHandler, Choose a route", reply_markup=reply_markup
    )
    return FIRST


def two(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("1", callback_data=str(ONE)),
            InlineKeyboardButton("3", callback_data=str(THREE)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Second CallbackQueryHandler, Choose a route", reply_markup=reply_markup
    )
    return FIRST


def three(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Yes, let's do it again!", callback_data=str(ONE)),
            InlineKeyboardButton("Nah, I've had enough ...", callback_data=str(TWO)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Third CallbackQueryHandler. Do want to start over?", reply_markup=reply_markup
    )
    # Transfer to conversation state `SECOND`
    return SECOND


def four(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("2", callback_data=str(TWO)),
            InlineKeyboardButton("3", callback_data=str(THREE)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Fourth CallbackQueryHandler, Choose a route", reply_markup=reply_markup
    )
    return FIRST


def end(update: Update, context: CallbackContext) -> int:
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
        entry_points=[CommandHandler('start', start)],
        states={
            FIRST: [
                CallbackQueryHandler(one, pattern='^' + str(ONE) + '$'),
                CallbackQueryHandler(two, pattern='^' + str(TWO) + '$'),
                CallbackQueryHandler(three, pattern='^' + str(THREE) + '$'),
                CallbackQueryHandler(four, pattern='^' + str(FOUR) + '$'),
            ],
            SECOND: [
                CallbackQueryHandler(start_over, pattern='^' + str(ONE) + '$'),
                CallbackQueryHandler(end, pattern='^' + str(TWO) + '$'),
            ],
        },
        fallbacks=[CommandHandler('start', start)],
    )

    # Add ConversationHandler to dispatcher that will be used for handling updates
    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()