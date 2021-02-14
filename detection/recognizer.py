import cv2
import numpy as np

class face_detection:
    names = [] 
    recognizer = None
    faceCascade = None
    cam = None
    minW = 0
    minH = 0

    def __init__(self, trainerfile, cascadepath, names, modelFile, configFile):
        self.names = names
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.faceCascade = cv2.CascadeClassifier(cascadepath)
        self.net = cv2.dnn.readNetFromTensorflow(modelFile, configFile)

        self.net.setPreferableBackend(cv2.dnn.DNN_TARGET_CPU)
        self.recognizer.read(trainerfile)
        self.cam = cv2.VideoCapture(0)
        self.cam.set(3, 640)
        self.cam.set(4, 480)
        self.minW = 0.1 * self.cam.get(3)
        self.minH = 0.1 * self.cam.get(4)

    # Returns a single frame from the camera
    def get_frame(self):
        ret, img = self.cam.read()
        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return img

    # Returns tuple of (boolean, [names]) where names are the faces detected
    # and boolean is whether a face is detected
    def get_face(self):
        gray = self.get_frame()
        faces = self.faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(int(self.minW), int(self.minH)),
        )
        return gray, faces

    def get_face_ssd(self):
        img = self.get_frame()    
        frameHeight = img.shape[0]
        frameWidth = img.shape[1]
        blob = cv2.dnn.blobFromImage(img, 1.0, (300,300), [104,117,123], False, False,)
        self.net.setInput(blob)
        detections = self.net.forward()
        faces = []
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.7:
                x1 = int(detections[0, 0, i, 3] * frameWidth)
                y1 = int(detections[0, 0, i, 4] * frameHeight)
                x2 = int(detections[0, 0, i, 5] * frameWidth)
                y2 = int(detections[0, 0, i, 6] * frameHeight)
                w = x2 - x1
                h = y2 - y1
                faces.append((x1, y1, w, h))
        return img, faces

    def recognise_face(self):
        img, faces = self.get_face_ssd()

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        detected_names = []

        for (x, y, w, h) in faces:
            id, confidence = self.recognizer.predict(gray[y:y+h, x:x+w])
            # If confidence is less them 100 ==> "0" : perfect match
            if (confidence < 70):
                detected_names.append(self.names[id])
                confidence = "  {0}%".format(round(100 - confidence))
            else:
                detected_names.append("unknown")
                confidence = "  {0}%".format(round(100 - confidence))

        if len(faces) != 0:
            return (True, detected_names)
        else:
            return (False, None)

    def stop(self):
        cam.release()

if __name__ == "__main__":

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('trainer/trainer.yml')
    cascadePath = "Cascades/haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)
    font = cv2.FONT_HERSHEY_SIMPLEX  # iniciate id counter
    id = 0  # names related to ids: example ==> Marcelo: id=1,  etc
    # Initialize and start realtime video capture
    names = ['None', 'Siyu', 'JQ', 'Sherwin', 'Tianyi']
    cam = cv2.VideoCapture(0)
    cam.set(3, 640)  # set video widht
    # set video height# Define min window size to be recognized as a face
    cam.set(4, 480)
    minW = 0.1*cam.get(3)
    minH = 0.1*cam.get(4)
    while True:
        ret, img = cam.read()
        # img = cv2.flip(img, -1) # Flip vertically
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(int(minW), int(minH)),
        )
        for(x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            id, confidence = recognizer.predict(gray[y:y+h, x:x+w])
            # If confidence is less them 100 ==> "0" : perfect match
            if (confidence < 100):
                id = names[id]
                confidence = "  {0}%".format(round(100 - confidence))
            else:
                id = "unknown"
                confidence = "  {0}%".format(round(100 - confidence))

            cv2.putText(
                img,
                str(id),
                (x+5, y-5),
                font,
                1,
                (255, 255, 255),
                2
            )
            cv2.putText(
                img,
                str(confidence),
                (x+5, y+h-5),
                font,
                1,
                (255, 255, 0),
                1
            )

        cv2.imshow('camera', img)
        k = cv2.waitKey(10) & 0xff  # Press 'ESC' for exiting video
        if k == 27:
            break  # Do a bit of cleanup

    print("\n [INFO] Exiting Program and cleanup stuff")
    cam.release()
    cv2.destroyAllWindows()