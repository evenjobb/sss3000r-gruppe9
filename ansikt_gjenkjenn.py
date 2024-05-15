import cv2
import numpy as np
import os 


id = 0
listeNavn = ['Ingen', 'Even', 'Sindre', 'Haroon', 'Z', 'W']
    
def ansikt_gjenkjenn():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('trainer/trainer.yml')
    cascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)

    img = cv2.imread("bilde.jpg")
    # flipper bildet
    img = cv2.flip(img, 0)

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale( 
        gray,
        scaleFactor = 1.2,
        minNeighbors = 5,
        minSize = (20, 20),
    )

    for (x, y, w, h) in faces:
        id, confidence = recognizer.predict(gray[y:y+h, x:x+w])

        if confidence < 100:
            if 0 <= id < len(listeNavn):
                navn = listeNavn[id]
                return True, navn
    
    return False, None
