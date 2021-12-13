from telegram import *
from requests import *
from telegram.ext import *
import test_bot_apikey as key

def error(update: Update, context: CallbackContext) -> None:
    print(f"Update {update} caused an error {context.error}")

def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("""
    
    /start -> starts me

/help -> this message

    """)

new_applicant = "I am a NEW applicant"
existing_applicant = "I am an existing applicant"
interviewer = "I am an interviewer"
    
new_applicant_instructions = "To create a profile click or type /insert"
existing_applicant_instructions = "Here is your profile, to edit, type /edit"
interviewer_instructions = "View applicant profile by typing in their telegram username"

def start_command(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton(text=new_applicant, callback_data=new_applicant_instructions),
            InlineKeyboardButton(text=existing_applicant, callback_data=existing_applicant_instructions),
        ],
        [InlineKeyboardButton(text=interviewer, callback_data=interviewer_instructions)],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose:', reply_markup=reply_markup)

def query_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    if query.data == existing_applicant_instructions:

        details = """
        
        Contact me @ 87654321
    
Reach me @ sohzi.hao@gmail.com
    
Connect with me on LinkedIn @ https://www.linkedin.com/in/sohzihao/
    
View my project @ https://ikanbilis99.github.io/v2_layout.html

        """
        context.bot.send_message(chat_id=update.effective_chat.id, text=details)
    
    if query.data == new_applicant_instructions or interviewer_instructions:
        
        query.edit_message_text(text=f"{query.data}")

    return


def main() -> None:
    updater = Updater(key.API_KEY)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CallbackQueryHandler(query_handler))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()

main()
