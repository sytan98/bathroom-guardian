from recognizer import face_detection
# from accel import accelerometer
import time

trainerfile = 'trainer/trainer.yml'
cascadepath = 'Cascades/haarcascade_frontalface_default.xml'
names = ['None', 'Siyu', 'JQ', 'Sherwin', 'Tianyi']

cv_instance = face_detection(trainerfile, cascadepath, names)
# accel_instance = accelerometer()

while True:
    has_face, names = cv_instance.get_face()
    print(has_face)
    print(names)
    time.sleep(0.5)