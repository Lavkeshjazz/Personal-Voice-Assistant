import speech_recognition as sr
import webbrowser   # Python can open browser
import pyttsx3      # Convert text to speech
import musicLibrary
import requests
import pygame
import os
from gtts import gTTS
#from openai import OpenAI

recognizer = sr.Recognizer()
ttsx = pyttsx3.init()  # Initialization


# This function will speak the text provided
def speak_old(text):
    ttsx.say(text)
    ttsx.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')
    # Initialize Pygame mixer
    pygame.mixer.init()
    # Load the MP3 file
    pygame.mixer.music.load('temp.mp3')
    # Play the MP3 file
    pygame.mixer.music.play()
    # Keep the program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.unload()
    os.remove("temp.mp3")


def aiProcess(command):
    client = OpenAI(api_key=api_AI)
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a virtual assistant, skilled in general tasks like Alexa, Siri and Google Assistant. Give short responses"},
            {"role": "user", "content": command}
        ]
    )
    return (completion.choices[0].message.content)

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            # Parse the JSON response
            data = r.json()
            articles = data.get('articles', [])
            # Print the headlines
            for article in articles:
                speak(article['title'])
    # else:
    #     output = aiProcess(c)
    #     speak(output)

if __name__ == "__main__":
    speak("Initializing....")
    while True:
        # Listen for the wake word "Hello Voice Assistant"
        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=2)
                # timeout will decide that after this many seconds if nothing is detected then timeout will occur
                # phrase_time_limit here checks for 5 sec after break in every statement, for 5 sec if nothing is said then the phrase said will be taken as input or if anything is said between these 5 sec then it will continue to listen
            word = recognizer.recognize_google(audio)
            print("You said: " + word)
            if word.lower() == "hello voice assistant":
                speak("Yes")
                # Listen for command
                with sr.Microphone() as source:
                    print("Voice Assistant Active....")
                    audio = recognizer.listen(source,timeout=4, phrase_time_limit=2)
                    command = recognizer.recognize_google(audio)
                    print(command)
                    processCommand(command)

        except Exception as e:
            print("Error; {0}".format(e))
