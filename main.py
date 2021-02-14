from recognizer import face_detection
# from accel import accelerometer
import time

trainerfile = 'trainer/trainer.yml'
cascadepath = 'Cascades/haarcascade_frontalface_default.xml'
names = ['None', 'Siyu', 'JQ', 'Sherwin', 'Tianyi']
modelfile =  "models/opencv_face_detector_uint8.pb"
configfile = "models/opencv_face_detector.pbtxt"

cv_instance = face_detection(trainerfile, cascadepath, names, modelfile, configfile)
# accel_instance = accelerometer()

while True:
    has_face, names = cv_instance.recognise_face()
    print(has_face)
    print(names)
    time.sleep(0.5)