import os
import logging

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

import openai
openai.api_key = os.getenv("OPENAI_API_KEY")

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

# Define a function for handling the /start command
def start(update: Update, _: CallbackContext) -> None:
    update.message.reply_text('Hi! I am a chatbot. How can I help you today?')

# Define a function for handling text messages
def echo(update: Update, _: CallbackContext) -> None:
    # Get the user's message
    message = update.message.text

    # Use OpenAI's GPT-3 to generate a response
    response = openai.Completion.create(
        engine="davinci",
        prompt=message,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )

    # Send the response to the user
    update.message.reply_text(response.choices[0].text)

def main() -> None:
    # Create an Updater object
    updater = Updater(os.getenv("TELEGRAM_TOKEN"))

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register handlers for the /start and text messages
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
    updater.idle()

if __name__ == '__main__':
    main()
