# voice_control.py

import threading
import speech_recognition as sr

latest_command = None  # shared variable

def voice_loop():
    global latest_command
    r = sr.Recognizer()

    while True:
        try:
            with sr.Microphone() as source:
                print("🎤 Listening...")
                audio = r.listen(source, phrase_time_limit=2)

            text = r.recognize_google(audio).lower()
            print("Heard:", text)

            latest_command = text

        except:
            pass

def listen_for_command():
    r = sr.Recognizer()

    with sr.Microphone() as source: # listens for reject
        print("Listening...")
        audio = r.listen(source, phrase_time_limit=2)

    try:
        text = r.recognize_google(audio).lower()
        print("Heard:", text)
        
        return text
    except:
        return None

