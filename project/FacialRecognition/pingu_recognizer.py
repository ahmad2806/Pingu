import cv2
import time
from collections import Counter


class PinguRecognizer(object):

    def __init__(self):
        self.predictions = []
        self.start = time.time()
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.recognizer.read('trainer/trainer.yml')
        self.cascadePath = "haarcascade_frontalface_default.xml"
        self.faceCascade = cv2.CascadeClassifier(self.cascadePath);

        self.font = cv2.FONT_HERSHEY_SIMPLEX

        self.id = 0

        self.names = ['Rabia', 'Ahmad', 'Rabia', 'Eyal', 'Ahmad', 'Udi']

        self.cam = cv2.VideoCapture(0)

        self.cam.set(3, 1024)
        self.cam.set(4, 782)

        self.minW = 0.1 * self.cam.get(3)
        self.minH = 0.1 * self.cam.get(4)

    def active(self):

        while True:
            time.sleep(0.3)
            ret, img = self.cam.read()

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            faces = self.faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=(int(self.minW), int(self.minH)),
            )

            for (x, y, w, h) in faces:

                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

                ID, confidence = self.recognizer.predict(gray[y:y + h, x:x + w])
                self.predictions.append(ID)
                if confidence < 100:
                    ID = self.names[ID]

                    confidence = "  {0}%".format(round(100 - confidence))
                else:
                    ID = "unknown"
                    confidence = "  {0}%".format(round(100 - confidence))

                cv2.putText(img, str(ID), (x + 5, y - 5), self.font, 1, (255, 255, 255), 2)
                cv2.putText(img, str(confidence), (x + 5, y + h - 5), self.font, 1, (255, 255, 0), 1)

                cv2.imshow('camera', img)

            k = cv2.waitKey(10) & 0xff
            if k == 27:
                break
            most_common, num_most_common = 0, 0
            try:
                most_common, num_most_common = Counter(self.predictions).most_common(1)[0]
            except:
                pass

            if time.time() - self.start > 10 and num_most_common > 15:
                return self.names[most_common]

    def deactivate(self):
        print("\n [INFO] Exiting Program and cleanup stuff")
        self.cam.release()
        cv2.destroyAllWindows()
