import speech_recognition as sr

def listen_for_command():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source, phrase_time_limit=2)

    try:
        text = r.recognize_google(audio).lower()
        print("Heard:", text)
        return text
    except:
        return None

