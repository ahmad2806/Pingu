import random

GREETINGS = [
    "Helloo",
    "Hiii",
    "Good Morning",
]
questions_lst = list()


GENERIC_QUESTIONS = [
    "How do you feel today?",
    "What makes you happy?",
    "What have your friends been up to?",
    "If you could do anything right now, what would you do?",
    "Do you ever think about renaming the colors of your crayons?",
    "What character makes you laugh the most?",
    "What makes you feel brave?",
    "If you could do anything right now, what would you do?",
    "What do you look forward to when you wake up?",
    "What character makes you laugh the most?",
    "Did you smile or laugh extra today?",
    "If you could do anything right now, what would you do?",
    "Describe a great day",
    " Do you like it when other people share with you? Why?",
    " Tell me something about you that you think I might not know.",
    " Did you have bad dreams?",
]
PATIENT_QUESTIONS = [
    "{}, do you still feel stressed?",
    "{}, did you talk with your friend Ahmad?",
    " How was your kindergarden today? {PATIENT_NAME}, ",
]

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
from collections import Counter

import time

import threading

import cv2

import speech_recognition as sr
import pyttsx3

sample_rate = 48000
chunk_size = 2048
r = sr.Recognizer()
r.dynamic_energy_threshold = True
# voices = engine.getProperty('voices')
# voice = voices[10]
WAIT_BOUND = 4


def listen():
    with sr.Microphone(device_index=0, sample_rate=sample_rate, chunk_size=chunk_size) as source:
        audio = r.listen(source=source, timeout=WAIT_BOUND, )
        return r.recognize_google(audio)


mutex = threading.Lock()

engine = pyttsx3.init()


def speak(text):
    global engine
    # mic_name = "Built-in Microphone"
    # sample_rate = 48000
    # chunk_size = 2048
    # WAIT_BOUND = 4
    # r = sr.Recognizer()
    # r.dynamic_energy_threshold = True
    engine.say(text)
    engine.runAndWait()


default_cap = cv2.VideoCapture('talk.mp4')


def default():
    global default_cap
    interframe_wait_ms = 30

    while default_cap.isOpened():

        cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("window", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        default_cap = cv2.VideoCapture('talk.mp4')

        while True:
            with mutex:
                ret, frame = default_cap.read()
            if not ret:
                print("Reached end of video, exiting.")
                break

            cv2.imshow("window", frame)
            if cv2.waitKey(interframe_wait_ms) & 0x7F == ord('q'):
                print("Exit requested.")
                break


def get_question(patient_name):
    i = random.randint(0, 1)
    return GENERIC_QUESTIONS[random.randint(0, len(GENERIC_QUESTIONS) - 1)] \
        if i == 0 else PATIENT_QUESTIONS[random.randint(0, len(PATIENT_QUESTIONS) - 1)].format(patient_name)

my_list = ["default.mp4", "talk.mp4"]
i = 0


def start_simulation(patient_name):
    talk_states = ["greet", "talk", "bye"]
    current_state = "greet"

    global default_cap

    t = threading.Thread(target=default)
    t.start()

    t2 = threading.Thread(target=emotion_detector)
    t2.daemon = True
    t2.start()

    questions_counter = 0

    i = 1
    while True:
        # time.sleep(0.5)
        if i == 0:
            print(listen())
            i = 1
        else:
            questions_counter += 1

            if questions_counter > 5:
                print(get_emotion())
                break

            if current_state == "greet":
                speak(GREETINGS[random.randint(0, len(GREETINGS) - 1)])
                current_state = "talk"
            elif current_state == "talk":
                speak("aaaaaaaa")

            i = 0

        with mutex:
            default_cap = cv2.VideoCapture(my_list[i])


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

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

                # cv2.imshow('camera', img)

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


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from collections import Counter

import numpy as np
import cv2
from keras.preprocessing import image

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)
from keras.models import model_from_json

model = model_from_json(open("facial_expression_model_structure.json", "r").read())
model.load_weights('facial_expression_model_weights.h5')  # load weights

# -----------------------------

emotions = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')

emotions_list = []


################################################################################################################################################
def emotion_detector():
    emotions_list = []
    while True:
        ret, img = cap.read()
        # img = cv2.imread('C:/Users/IS96273/Desktop/hababam.jpg')

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        # print(faces) #locations of detected faces

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)  # draw rectangle to main image

            detected_face = img[int(y):int(y + h), int(x):int(x + w)]  # crop detected face
            detected_face = cv2.cvtColor(detected_face, cv2.COLOR_BGR2GRAY)  # transform to gray scale
            detected_face = cv2.resize(detected_face, (48, 48))  # resize to 48x48

            img_pixels = image.img_to_array(detected_face)
            img_pixels = np.expand_dims(img_pixels, axis=0)

            img_pixels /= 255  # pixels are in scale of [0, 255]. normalize all pixels in scale of [0, 1]

            predictions = model.predict(img_pixels)  # store probabilities of 7 expressions

            # find max indexed array 0: angry, 1:disgust, 2:fear, 3:happy, 4:sad, 5:surprise, 6:neutral
            max_index = np.argmax(predictions[0])

            emotion = emotions[int(max_index)]

            emotions_list.append(int(max_index))

        # -------------------------

        # cv2.imshow('img', img)

        if cv2.waitKey(1) & 0xFF == ord('q'):  # press q to quit
            break


################################################################################################################################################

def get_emotion():
    most_common, num_most_common = 0, 0
    try:
        most_common, num_most_common = Counter(emotions_list).most_common(1)[0]
    except:
        pass
    return emotions[most_common]


def start_simulation(patient_name):
    talk_states = ["greet", "talk", "bye"]
    current_state = "greet"

    global default_cap

    t = threading.Thread(target=default)
    t.start()

    t2 = threading.Thread(target=emotion_detector)
    t2.daemon = True
    t2.start()

    questions_counter = 0

    i = 1
    while True:
        # time.sleep(0.5)
        if i == 0:
            print(listen())
            i = 1
        else:
            questions_counter += 1

            if questions_counter > 5:
                print(get_emotion())
                break

            if current_state == "greet":
                speak(GREETINGS[random.randint(0, len(GREETINGS) - 1)])
                current_state = "talk"
            elif current_state == "talk":
                speak(get_question())

            i = 0

        with mutex:
            default_cap = cv2.VideoCapture(my_list[i])


################################################################################################################################################
def main():
    recognizer = PinguRecognizer()
    while True:
        predection = recognizer.active()
        start_simulation(predection)


if __name__ == '__main__':
    main()
