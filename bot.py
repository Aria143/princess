import logging
import os
from telegram.ext import Updater, MessageHandler, Filters
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
def handle_message(update, context):
    text = update.message.text
    response = generate_response(text)
    update.message.reply_text(response)

def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Set up the Telegram bot
    updater = Updater(token=os.environ.get('TELEGRAM_TOKEN'), use_context=True)
    dispatcher = updater.dispatcher

    # Add the message handler to the dispatcher
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Start the bot
    updater.start_webhook(listen="0.0.0.0", port=int(os.environ.get('PORT', 5000)), url_path=os.environ.get('TELEGRAM_TOKEN'))
    updater.bot.setWebhook(os.environ.get('APP_URL') + os.environ.get('TELEGRAM_TOKEN'))
    logger.info("Bot started")

    # Run the bot until you press Ctrl-C or the process is stopped
    updater.idle()

if __name__ == '__main__':
    main()
