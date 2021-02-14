import secret
from multiprocessing.connection import Client

def sendMessage(message: str):
    address = ("localhost", secret.MESSAGE_PORT)
    conn = Client(address, authkey=secret.AUTH_KEY)
    conn.send(message)
    conn.close()

if __name__ == "__main__":
    while True:
        arg = input("Enter message: ")
        sendMessage(arg)