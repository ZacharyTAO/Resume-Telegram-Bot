from os import link
from typing import Callable

from telegram.message import Message
from dbhelper2 import DBHelper 
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, replymarkup, user
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
TOKEN = '5093335972:AAF5XKRoWd9AEVycikG7CzPljBo8RpKqBtE'

# Stages
CREATEPROFILE, ADDPHONE, MESSAGE, FIRST, SECOND, THIRD, FOURTH, EDIT_NAME, EDIT_MOBILE, EDIT_EMAIL, ADD_LINK_DESC, ADD_LINK_URL, EDIT_LINK_DESC, EDIT_LINK_URL = range(14)
# Callback data
PARTICULARS, LINKS, QNA, FOUR , BACK, QUIT, NAME, MOBILENUMBER, EMAIL, Q1, Q2, Q3, Q4, NEWLINK = range(14)

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
    update.message.reply_text("What would you like to edit?", reply_markup=reply_markup)
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

    query.edit_message_text(text="What details would you liked to edit?", reply_markup=reply_markup)
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
# Displays the user's prticulars and the necessary edit buttons
def particulars(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    username = query.message.chat.username
    user_particulars = db.get_profile(username)[0]
    fullname = user_particulars['fullname']
    contact_no = user_particulars['contact_no']
    email = user_particulars['email']
    msg = 'Name: <b>'+fullname+'</b>\nPhone: <b>'+contact_no+'</b>\nEmail: <b>'+email+'</b>'
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
        text=msg, reply_markup=reply_markup, parse_mode='html'
    )
# goes to second state
    return SECOND

# Displays the user's fullname and prompts them to edit if they wish
def name(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    username = query.message.chat.username
    user_particulars = db.get_profile(username)[0]
    fullname = user_particulars['fullname']
    msg = "You currently have your fullname stored as <b>" + fullname + "</b>\n" + \
    "If you would like to change it, type your name in and press enter"
    keyboard = [
        [
            InlineKeyboardButton("Back", callback_data=str(PARTICULARS)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text=msg, reply_markup=reply_markup, parse_mode='html'
    )
    return EDIT_NAME

# 
def edit_name(update: Update, context: CallbackContext) -> int:
    fullname = update.message.text
    username = update.message.chat.username
    db.update_name_profile(username, fullname)
    return SECOND

def mobilenumber(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    username = query.message.chat.username
    user_particulars = db.get_profile(username)[0]
    contact_no = user_particulars['contact_no']
    msg = "You currently have your contact number stored as <b>" + contact_no + "</b>\n" + \
    "If you would like to change it, type your contact number in and press enter"
    keyboard = [
        [
            InlineKeyboardButton("Back", callback_data=str(PARTICULARS)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text=msg, reply_markup=reply_markup, parse_mode='html'
    )
    return EDIT_MOBILE

def edit_mobile(update: Update, context: CallbackContext) -> int:
    contact_no = update.message.text
    username = update.message.chat.username
    db.update_number_profile(username, contact_no)
    return SECOND

def email(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    username = query.message.chat.username
    user_particulars = db.get_profile(username)[0]
    email = user_particulars['email']
    msg = "You currently have your email stored as <b>" + email + "</b>\n" + \
    "If you would like to change it, type your name in and press enter"
    keyboard = [
        [
            InlineKeyboardButton("Back", callback_data=str(PARTICULARS)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text=msg, reply_markup=reply_markup, parse_mode='html'
    )
    return EDIT_EMAIL

def edit_email(update: Update, context: CallbackContext) -> int:
    email = update.message.text
    username = update.message.chat.username
    db.update_email_profile(username, email)
    return SECOND

###

### FOR LINK FUNCTIONS ###
def links(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    username = query.message.chat.username
    user_links = db.get_links(username)
    msg = 'Add new links or edit your existing links here (maximum 4):\n\n'
    for link in user_links:
        msg += "<b>"+link["link_description"]+"</b>: "
        msg += link["link"] + "\n\n"

    # InlineKeyboardButtons will be created for each existing link with the tag "Edit [Link_Description]"
    # There will be an 'Add a New Link' button to create new links
    # [{link_description: Github, link:},{})
    keyboard = [[]]
    num_links = len(user_links)
    for i in range(num_links):
        keyboard[0].append(InlineKeyboardButton("Edit " + user_links[i]["link_description"], callback_data="LINK_"+user_links[i]["link_description"])) #user_links[i] refers to one dictonary #user_links[i][link_description] gets the name of the description
    keyboard.append([InlineKeyboardButton("Add a New Link", callback_data=str(NEWLINK))])
    keyboard.append(
        [
            InlineKeyboardButton("Back", callback_data=str(BACK)),
            InlineKeyboardButton("End", callback_data=str(QUIT)),
        ]
    )
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text=msg, reply_markup=reply_markup, parse_mode='html',disable_web_page_preview=True
    )
    # goes to third state
    return THIRD

# This function creates a new link and enters into the add link description state
def newlink(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    msg = "To create a new link, first send in a short description of the link.\n" + \
        "(for example, 'Github') or press 'Back' to return to view your existing links"
    keyboard = [
        [
            InlineKeyboardButton("Back", callback_data=str(LINKS)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text=msg, reply_markup=reply_markup
    )
    return ADD_LINK_DESC

# This function retrieves the new link desciption
def add_link_desc(update: Update, context: CallbackContext):
    new_link_desc = update.message.text
    username = update.message.chat.username
    keyboard = [
        [
            InlineKeyboardButton("Back", callback_data=str(LINKS)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    msg = "Next, please enter the URL for your given link description"
    update.message.reply_text(text=msg, reply_markup=reply_markup)
    context.user_data["link_description"] = new_link_desc
    return ADD_LINK_URL

# This function allows the user to edit or delete an existing link


# This function retrieves the new link url and inserts a new row into the database
def add_link_url(update: Update, context: CallbackContext):
    link_url = update.message.text
    username = update.message.chat.username
    link_description = context.user_data['link_description']
    logger.info(link_description)
    db.add_link(username, link_description, link_url)
    msg = "Your link for <b>" + link_description + "</b> has been added."
    update.message.reply_text(text=msg,  parse_mode='html')
    keyboard = [
        [
            InlineKeyboardButton("Back", callback_data=str(LINKS)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    return THIRD

# This function edits an existing link 
def editlink(update: Update, context: CallbackContext):
    logger.info("Testing to see if we reach this state.")
    data = update.callback_query.data 
    
    query = update.callback_query
    query.answer()
    link_description_old = data[5:] #LINK_doggo pic - get doggo pic
    # logger.info(link_description)
    username = query.message.chat.username
    link_url = db.get_link_url(username, link_description_old)
    msg = "Your current link description is <b>" + link_description_old + "</b>\n" + \
        "If you would like to change the link description, you can key a new one. Or else just press enter to edit the URL in the next step."
    keyboard = [
        [
            InlineKeyboardButton("Back", callback_data=str(LINKS)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=msg, reply_markup=reply_markup, parse_mode='html') #edit own text 

    
    context.user_data['link_description_old'] = link_description_old #saving into telegram bot memory 
    context.user_data['link_url'] = link_url
    return EDIT_LINK_DESC

def edit_name(update: Update, context: CallbackContext) -> int:
    fullname = update.message.text #user input
    username = update.message.chat.username #get current username
    db.update_name_profile(username, fullname)
    return SECOND

# This function retrieves the new link description
def edit_link_desc(update: Update, context: CallbackContext):
    logger.info("We are currently in this state")
    new_link_desc = update.message.text
    username = update.message.chat.username
    
    # if the user does not send anything, the link description is not edited
    if new_link_desc != '':
        context.user_data['link_description_new'] = new_link_desc #saving new link description to telegram memory state
    msg = "Next, please enter the URL for your given link description"
    keyboard = [
        [
            InlineKeyboardButton("Back", callback_data=str(LINKS)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(text=msg, reply_markup=reply_markup)
    return EDIT_LINK_URL

def edit_link_url(update: Update, context: CallbackContext):
    logger.info('Testing edit_link_url')
    link_url = update.message.text
    if link_url == '':
        link_url = context.user_data['link_url']
    username = update.message.chat.username
    link_description_old = context.user_data['link_description_old']
    link_description_new = context.user_data['link_description_new']

    logger.info(link_description_old)
    logger.info(link_description_new)
    db.edit_link(username, link_description_old, link_description_new, link_url)
    
    msg = "Your link for <b>" + link_description_new + "</b> has been added."
    update.message.reply_text(text=msg,  parse_mode='html')
    msg = "Your new link is " + link_description_new + "and" + link_url

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
def error(update: Update, context: CallbackContext):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


### FOR MAIN FUNCTION TO RUN THE BOT###
def main() -> None:
    updater = Updater(TOKEN)
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
            # State for handling all particulars
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
                CallbackQueryHandler(editlink, pattern='^' + "LINK_"),
                CallbackQueryHandler(newlink, pattern='^' + str(NEWLINK) + '$'),
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
            EDIT_NAME:[
                MessageHandler(Filters.text & ~Filters.command, edit_name),
                CallbackQueryHandler(particulars, pattern='^' + str(PARTICULARS) + '$'),
            ],
            EDIT_MOBILE:[
                MessageHandler(Filters.text & ~Filters.command, edit_mobile),
                CallbackQueryHandler(particulars, pattern='^' + str(PARTICULARS) + '$'),
            ],
            EDIT_EMAIL:[
                MessageHandler(Filters.text & ~Filters.command, edit_email),
                CallbackQueryHandler(particulars, pattern='^' + str(PARTICULARS) + '$'),
            ],
            ADD_LINK_DESC:[
                MessageHandler(Filters.text & ~Filters.command, add_link_desc),
                CallbackQueryHandler(links, pattern='^' + str(LINKS) + '$'),
            ],
            ADD_LINK_URL:[
                MessageHandler(Filters.text & ~Filters.command, add_link_url),
                CallbackQueryHandler(links, pattern='^' + str(LINKS) + '$'),
            ],
            EDIT_LINK_DESC:[
                MessageHandler(Filters.text & ~Filters.command, edit_link_desc),
                CallbackQueryHandler(links, pattern='^' + str(LINKS) + '$'),
            ],
            EDIT_LINK_URL:[
                MessageHandler(Filters.text & ~Filters.command, edit_link_url),
                CallbackQueryHandler(links, pattern='^' + str(LINKS) + '$'),
            ],

        },
        fallbacks=[CommandHandler('edit', main_menu), CommandHandler('start', start)],
    )

    # Add ConversationHandler to dispatcher that will be used for handling updates
    dispatcher.add_handler(conv_handler1)
    dispatcher.add_handler(conv_handler2)
    dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()