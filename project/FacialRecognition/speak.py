
import pyttsx3
import speech_recognition as sr


def speak(text):
    mic_name = "Built-in Microphone"
    sample_rate = 48000
    chunk_size = 2048
    r = sr.Recognizer()
    r.dynamic_energy_threshold = True
    engine = pyttsx3.init()
    WAIT_BOUND = 4
    engine.say(f'{text}')
    engine.runAndWait()


