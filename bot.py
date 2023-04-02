import os
import telegram
from telegram.ext import Updater, MessageHandler, Filters
from transformers import pipeline

# Get the Telegram bot token from the environment variable
TOKEN = os.environ.get('TOKEN')

# Create the Telegram bot object
bot = telegram.Bot(token=TOKEN)

# Define the message handler
def generate_response(update, context):
    # Get the user's message text
    user_message = update.message.text

    # Use ChatGPT to generate a response
    chatgpt = pipeline('text-generation', model='EleutherAI/gpt-neo-2.7B')
    response = chatgpt(user_message, max_length=50)[0]['generated_text']

    # Send the response back to the user
    context.bot.send_message(chat_id=update.effective_chat.id, text=response)

# Create the updater and dispatcher objects
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Add the message handler to the dispatcher
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, generate_response))

# Start the bot
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    updater.start_webhook(listen="0.0.0.0", port=port, url_path=TOKEN)
    updater.bot.setWebhook("https://queenprincess.herokuapp.com/" + TOKEN)
    updater.idle()
