import os
import logging
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import openai

openai.api_key = os.environ.get('OPENAI_API_KEY')

# Define the function that will generate the response from ChatGPT
def generate_response(text):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=text,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7
    )
    message = response.choices[0].text.strip()
    return message

# Define the function that will handle incoming messages from the user
def handle_message(update: Update, context):
    text = update.message.text
    response = generate_response(text)
    update.message.reply_text(response)

# Define the /start command handler
def start(update: Update, context):
    update.message.reply_text("Hello! I am a ChatGPT bot. Send me a message and I will respond with a generated text.")

def main():
    # Set up logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    # Set up the Telegram bot
    updater = Updater(token=os.environ.get('TELEGRAM_TOKEN'), use_context=True)
    dispatcher = updater.dispatcher

    # Add the command handlers
    dispatcher.add_handler(CommandHandler("start", start))

    # Add the message handler to the dispatcher
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Start the bot
    updater.start_polling()
    logging.info("Bot started")

    # Run the bot until you press Ctrl-C or the process is stopped
    updater.idle()

if __name__ == '__main__':
    main()
