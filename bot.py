import os
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, MessageFilter

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Set up the bot
updater = Updater(token=os.environ.get('TOKEN'), use_context=True)
dispatcher = updater.dispatcher

# Define the message filter
class AllMessageFilter(MessageFilter):
    def filter(self, message):
        return True

# Define the handler function
def chat_gpt_handler(update, context):
    # Get the user's message
    message = update.message.text

    # Generate a response using ChatGPT
    response = "This is a ChatGPT response to: " + message

    # Send the response back to the user
    context.bot.send_message(chat_id=update.effective_chat.id, text=response)

# Create the handler and add it to the dispatcher
message_handler = MessageHandler(AllMessageFilter(), chat_gpt_handler)
dispatcher.add_handler(message_handler)

# Start the bot
updater.start_polling()
updater.idle()
