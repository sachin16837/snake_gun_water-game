import speech_recognition as sr
import webbrowser
import pyttsx3
import time
import musiclibrary  # your custom dictionary of songs

recognizer = sr.Recognizer()

def speak(text):
    """Text-to-speech function"""
    print(f"[Jarvis will say] {text}")
    engine = pyttsx3.init('sapi5')  # re-init each time
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 170)
    engine.say(text)
    engine.runAndWait()
    engine.stop()

def ProcessCommand(c):
    """Handle user commands"""
    c = c.lower()
    if "open google" in c:
        speak("Opening Google")
        webbrowser.open("https://google.com")
    elif "open youtube" in c:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")
    elif "open facebook" in c:
        speak("Opening Facebook")
        webbrowser.open("https://facebook.com")
    elif "open linkdin" in c:
        speak("Opening Facebook")
        webbrowser.open("https://linkedin.com")
    elif c.startswith("play"):
        try:
            song = c.replace("play", "", 1).strip().lower()  # normalize input
        # convert dictionary keys to lowercase before searching
            if song in (key.lower() for key in musiclibrary.music.keys()):
            # find the exact matching key (case-insensitive)
                for key, link in musiclibrary.music.items():
                    if key.lower() == song:
                        speak(f"Playing {key}")
                        webbrowser.open(link)
                        break
            else:
                speak(f"Sorry, I could not find {song} in the library.")
        except Exception as e:
            speak("Sorry, I could not play that song.")
            print(f"[Error in music] {e}")


if __name__ == "__main__":
    speak("Initializing Jarvis...")

    while True:
        try:
            # listen for wake word
            with sr.Microphone() as source:
                print("Listening ")
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=2)

            word = recognizer.recognize_google(audio)
            print(f"Heard: {word}")

            if "jarvis" in word.lower():
                speak("Yes")
                time.sleep(0.5)  # let TTS finish before mic opens

                with sr.Microphone() as source:
                    print("Jarvis active")
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = recognizer.listen(source, timeout=3, phrase_time_limit=5)

                command = recognizer.recognize_google(audio)
                print(f"You said: {command}")
                ProcessCommand(command)

        except sr.WaitTimeoutError:
            # No speech detected, just continue loop
            continue
        except sr.UnknownValueError:
            # Could not understand speech
            print("Didn't catch that...")
            continue
        except Exception as e:
            print(f"[Error] {e}")
            continue
