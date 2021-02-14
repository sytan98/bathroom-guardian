from telegram.ext import (Updater, CommandHandler, MessageHandler, 
                          ConversationHandler, Filters)
import secret
import pickle
import os

PRE_AUTH, POST_AUTH = range(2)

class telegramNotifierBot():

    def __init__(self):
        self.chatIds = []
        self.botInstance = None

    def start(self, update, context):
        self.botInstance = context.bot
        self.botInstance.send_message(update.effective_chat.id,
                                text="Welcome! Please enter the password.")

        return PRE_AUTH

    def authUser(self, update, context):
        if update.message.text == secret.PASSWORD:
            chatId = update.effective_chat.id
            if chatId not in self.chatIds:
                self.chatIds.append(chatId)

            update.message.reply_text("Welcome!")
            return POST_AUTH
        else:
            update.message.reply_text("I told you it does nothing.")
            return PRE_AUTH

    def echo(self, update, context):
        update.message.reply_text(update.message.text)

    def cancel(self, update, context):
        update.message.reply_text('Bye!')

        return ConversationHandler.END


    # "Public" methods
    def sendTelegramMessage(self, message: str):
        if self.botInstance:
            for chatId in self.chatIds:
                self.botInstance.send_message(chatId, text=message)
        else:
            print("Please start the bot with /start!")

    def startTelegramBot(self):
        conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', self.start)],
        states={
            PRE_AUTH: [MessageHandler(Filters.text & (~Filters.command), self.authUser)],
            POST_AUTH: [MessageHandler(Filters.text & (~Filters.command), self.echo)],
        },
        fallbacks=[CommandHandler('cancel', self.cancel)])

        # Load previous chatIds
        filepath = secret.PICKLE_FILEPATH
        if os.path.isfile(filepath):
            with open(filepath, 'rb') as pfile:
                self.chatIds = pickle.load(pfile)

        # Set up bot
        self.updater = Updater(token=secret.BOT_TOKEN, use_context=True)
        dispatcher = self.updater.dispatcher
        dispatcher.add_handler(conv_handler)
        self.updater.start_polling()

    def stopTelegramBot(self):
        print("Saving chatIds to file...")
        with open(secret.PICKLE_FILEPATH, 'wb') as pfile:
                pickle.dump(self.chatIds, pfile)

        print("Stopping telegram bot...")
        self.updater.stop()