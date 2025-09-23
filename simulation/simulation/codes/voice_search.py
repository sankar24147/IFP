'''
import speech_recognition as sr
import webbrowser
import pyttsx3

# Initialize the recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    print(f"🔊 {text}")
    engine.say(text)
    engine.runAndWait()

def voice_search():
    with sr.Microphone() as source:
        speak("Listening... Please say your search query.")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        query = recognizer.recognize_google(audio)
        speak(f"You said: {query}")
    except sr.UnknownValueError:
        speak("Sorry, I could not understand the audio.")
    except sr.RequestError:
        speak("Could not request results from Google Speech Recognition service.")

if __name__ == "__main__":
    voice_search()
'''


import speech_recognition as sr
import webbrowser
import pyttsx3

# Initialize the recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    print(f"🔊 {text}")
    engine.say(text)
    engine.runAndWait()

def voice_search():
    print("This is voice search AAAAAAAAAAAAAAAAAAAAAAA")
    with sr.Microphone() as source:
        speak("Listening... Please say your search query.")
        recognizer.adjust_for_ambient_noise(source)

        try:
            # Wait max 5 sec for speech to start, listen max 5 sec
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
        except sr.WaitTimeoutError:
            return "You didn't say anything. Please try again."
            

    try:
        query = recognizer.recognize_google(audio)
        speak(f"You said: {query}")
        # Example: open Google search in browser
        webbrowser.open(f"https://www.google.com/search?q={query}")
    except sr.UnknownValueError:
        return "Sorry, I could not understand the audio."
    except sr.RequestError:
        return "Could not request results from Google Speech Recognition service."

if __name__ == "__main__":
    voice_search()