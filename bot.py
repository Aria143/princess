import os
import telegram
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater
import openai
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

# Configure OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define command handlers
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi! I am a language model powered by OpenAI. You can chat with me by sending a message!')

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('You can chat with me by sending a message!')

def chat(update, context):
    """Reply to user message."""
    # Get user message
    user_message = update.message.text

    # Generate response using ChatGPT
    response = openai.Completion.create(
        engine="davinci",
        prompt=user_message,
        max_tokens=1024,
        temperature=0.5,
    )

    # Send response
    update.message.reply_text(response.choices[0].text)

def main():
    # Create Telegram bot
    updater = Updater(os.getenv("TELEGRAM_BOT_TOKEN"), use_context=True)
    dispatcher = updater.dispatcher

    # Define handlers
    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', help)
    chat_handler = MessageHandler(Filters.text & ~Filters.command, chat)

    # Add handlers to dispatcher
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(chat_handler)

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
