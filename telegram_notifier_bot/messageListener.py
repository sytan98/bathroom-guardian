import secret
from typing import Callable
from multiprocessing.connection import Listener

class messageListener():
    def __init__(self):
        self.listener = None

    def startListener(self, messageConsumer: Callable[[str], None]):
        address = ("localhost", secret.MESSAGE_PORT)
        self.listener = Listener(address, authkey=secret.AUTH_KEY)

        while True:
            conn = self.listener.accept()
            message = conn.recv()
            messageConsumer(message)

    def stopListener(self):
        print("Stopping listener!")
        self.listener.close()