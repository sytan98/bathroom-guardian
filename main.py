from recognizer import face_detection


cv = face_detection('trainer/trainer.yml', 
                    "Cascades/haarcascade_frontalface_default.xml", )
