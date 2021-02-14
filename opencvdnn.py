import cv2
import numpy

modelFile = "models/opencv_face_detector_uint8.pb"
configFile = "models/opencv_face_detector.pbtxt"
net = cv2.dnn.readNetFromTensorflow(modelFile, configFile)

net.setPreferableBackend(cv2.dnn.DNN_TARGET_CPU)

cam = cv2.VideoCapture(0)
cam.set(3, 640)  # set video widht
# set video height# Define min window size to be recognized as a face
cam.set(4, 480)
minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)
while True:
    ret, img = cam.read()
    # img = cv2.flip(img, -1) # Flip vertically
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    frameHeight = img.shape[0]
    frameWidth = img.shape[1]
    blob = cv2.dnn.blobFromImage(img, 1.0, (300,300), [104,117,123], False, False,)
    net.setInput(blob)
    detections = net.forward()
    print(detections)
    bboxes = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.7:
            x1 = int(detections[0, 0, i, 3] * frameWidth)
            y1 = int(detections[0, 0, i, 4] * frameHeight)
            x2 = int(detections[0, 0, i, 5] * frameWidth)
            y2 = int(detections[0, 0, i, 6] * frameHeight)
            bboxes.append([x1, y1, x2, y2])
            cv2.rectangle(
                img,
                (x1, y1),
                (x2, y2),
                (255, 255, 255),
                int(round(frameHeight / 150)),
                8,
            )
    

    cv2.imshow('camera', img)
    k = cv2.waitKey(10) & 0xff  # Press 'ESC' for exiting video
    if k == 27:
        break  # Do a bit of cleanup

print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()