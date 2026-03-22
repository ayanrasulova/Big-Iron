import speech_recognition as sr
from queue import Queue

# Thread-safe queue for passing commands to main thread
command_queue = Queue()

def voice_loop():
    """
    Runs continuously in a background thread.
    Listens to microphone and pushes recognized commands into a queue.
    """
    r = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("🎤 Voice thread started and listening...")

            # optional: adjust for ambient noise
            r.adjust_for_ambient_noise(source, duration=1)

            while True:
                try:
                    audio = r.listen(source, phrase_time_limit=2)

                    text = r.recognize_google(audio).lower()
                    print("Heard:", text)

                    command_queue.put(text)

                except sr.UnknownValueError:
                    # speech not understood (normal)
                    continue

                except sr.RequestError as e:
                    print("Speech recognition API error:", e)

                except Exception as e:
                    print("Voice loop error:", e)

    except Exception as e:
        print("Microphone initialization failed:", e)


def get_latest_command():
    """
    Non-blocking fetch of the most recent command.
    Returns None if no command is available.
    """
    if not command_queue.empty():
        return command_queue.get()
    return None


def listen_for_command():
    """
    One-shot blocking listen (useful for specific triggers like 'reject').
    """
    r = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("🎤 Listening (one-shot)...")
            audio = r.listen(source, phrase_time_limit=2)

        text = r.recognize_google(audio).lower()
        print("Heard:", text)
        return text

    except Exception as e:
        print("One-shot listen error:", e)
        return None