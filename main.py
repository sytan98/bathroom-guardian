from detection.recognizer import face_detection
import RPi.GPIO as GPIO
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

# GPIO setup
GPIO.setmode(GPIO.BOARD)
channel = 31
GPIO.setup(channel, GPIO.IN)

cv_instance = face_detection(trainerfile, cascadepath, names)

while True:
    has_face, names = cv_instance.get_face()
    message = str(has_face) + str(names)

    if (GPIO.input(channel) == 1 and has_face):
        print(str(names) + "detected!")
        sendMessage(names + " detected!")
    else:
        print("No face detected!")
        sendMessage("No face detected!")
    
    time.sleep(0.5)