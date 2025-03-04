import speech_recognition as sr
import pyttsx3
from llm import invoke_llm

listener = sr.Recognizer()
player = pyttsx3.init()


def listen():
    with sr.Microphone() as input_device:
        print("I am ready, Listening ....")
        try:
            voice_content = listener.listen(input_device)
            text_command = listener.recognize_google(voice_content)
            print(text_command)
            return text_command
        except sr.UnknownValueError:
            print("Sorry, I did not understand the audio.")
            return None
        except sr.RequestError as e:
            print(f"Request failed; {e}")
            return None

def talk(text):
    player.say(text)
    player.runAndWait()

def run_voice_bot():
    while True:
        command = listen()
        if command:
            print(command)
            res = invoke_llm(command)
            talk(res)
        else:
            talk("Sorry, I couldn't hear you clearly. Please try again.")



run_voice_bot()
