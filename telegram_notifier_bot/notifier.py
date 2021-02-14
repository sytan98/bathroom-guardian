import threading
import atexit
from telegramBot import telegramNotifierBot
from messageListener import messageListener

# Include these in your secret.py files:
# MESSAGE_PORT    : int    Port to communicate between client and listener
# BOT_TOKEN       : str    Obtained from telegram botfather)
# PICKLE_FILEPATH : str    Stores list of users that have successfully authenticated )
# AUTH_KEY        : bytes  Instantiate as such b'your-key-here'
# PASSWORD        : str    User chosen password to authenticate on telegram

botInstance = telegramNotifierBot()
listenerInstance = messageListener()
telegrambotThread = threading.Thread(target=botInstance.startTelegramBot)
listenerThread = threading.Thread(target=listenerInstance.startListener, 
                                  args=[botInstance.sendTelegramMessage])

@atexit.register
def onExit():
    listenerInstance.stopListener()
    botInstance.stopTelegramBot()

if __name__ == "__main__":
    telegrambotThread.start()
    listenerThread.start()