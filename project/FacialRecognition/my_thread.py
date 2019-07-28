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
        try:
            audio = r.listen(source=source, timeout=WAIT_BOUND, )
            return r.recognize_google(audio)
        except sr.UnknownValueError or sr.WaitTimeoutError or sr.RequestError as e:
            return "No response"


import time
import random

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


default_cap = cv2.VideoCapture('default.mp4')


def default():
    global default_cap
    interframe_wait_ms = 30

    while default_cap.isOpened():

        cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("window", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        default_cap = cv2.VideoCapture('default.mp4')

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

    # default_cap.release()
    # # talk_cap.release()
    # cv2.destroyAllWindows()


class PatientInteractor:

    def __init__(self):
        self.state = "GREET"

    def ask_patient(self, text: str):
        q = ""

        # if self.state == "GREET":
        #     q = GREETINGS[random.randint(0, len(GREETINGS) - 1)]
        #     self.state = "TALK"
        # elif self.state == "TALK":
        #     q = GENERIC_QUESTIONS[random.randint(0, len(GENERIC_QUESTIONS) - 1)]

        # speak(q)

    def get_patient_response(self):
        pass
        # return listen()


def change_state():
    pass


my_list = ["small.mp4", "default.mp4"]
i = 0


def main():
    global default_cap
    # interacor = PatientInteractor()
    # animator = Animator()

    t = threading.Thread(target=default)
    t.start()
    i = 0
    while True:
        # time.sleep(0.5)
        if i == 0:
            speak("Hello")
            i = 1
        else:
            listen()
            i = 0

        with mutex:
            default_cap = cv2.VideoCapture(my_list[i])


if __name__ == '__main__':
    main()
