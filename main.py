from detection.recognizer import face_detection
# from accel import accelerometer
import time
from telegram_notifier_bot import secret
from multiprocessing.connection import Client

def sendMessage(message: str):
    address = ("localhost", secret.MESSAGE_PORT)
    conn = Client(address, authkey=secret.AUTH_KEY)
    conn.send(message)
    conn.close()

trainerfile = 'detection/trainer/trainer.yml'
cascadepath = 'detection/Cascades/haarcascade_frontalface_default.xml'
names = ['None', 'Siyu', 'JQ', 'Sherwin', 'Tianyi']

cv_instance = face_detection(trainerfile, cascadepath, names)
# accel_instance = accelerometer()

while True:
    has_face, names = cv_instance.get_face()
    message = str(has_face) + str(names)
    print(message)
    sendMessage(message)
    time.sleep(0.5)