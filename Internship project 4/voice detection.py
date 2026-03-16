import speech_recognition as sr
import webbrowser
import time
import playsound3
import os
import random
import requests
import geocoder
from gtts import gTTS
from time import ctime

r = sr.Recognizer()



# ================= SPEAK =================
def alexis_speak(audio_string):
    tts = gTTS(text=audio_string, lang='en')
    r_num = random.randint(1, 1000000)
    audio_file = f'audio-{r_num}.mp3'
    tts.save(audio_file)
    playsound3.playsound(audio_file)
    print(audio_string)
    os.remove(audio_file)

# ================= LISTEN =================
def record_audio(ask=False):
    with sr.Microphone() as source:
        if ask:
            alexis_speak(ask)

        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)

        voice_data = ''
        try:
            voice_data = r.recognize_google(audio).lower()
        except sr.UnknownValueError:
            alexis_speak("Sorry, I didn't understand")
        except sr.RequestError:
            alexis_speak("Speech service is down")

        return voice_data

# ================= WEATHER =================
def get_weather():
    g = geocoder.ip('me')
    city = g.city

    if not city:
        alexis_speak("I couldn't detect your location")
        return

    API_KEY = "f61588f8bbe24cbfb5defe7832411672"  # 🔴 OpenWeatherMap API Key
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        data = requests.get(url).json()
        if data.get("cod") != 200:
            alexis_speak("Unable to fetch weather")
            return

        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]

        alexis_speak(f"The temperature in {city} is {temp} degrees with {desc}")
    except:
        alexis_speak("Weather service error")

# ================= WIKIPEDIA (GOOGLE) =================
def open_wikipedia(topic):
    alexis_speak(f"Opening Wikipedia for {topic}")
    webbrowser.open(f"https://www.google.com/search?q=site:wikipedia.org+{topic}")

# ================= YOUTUBE =================
def play_song(song):
    alexis_speak(f"Playing {song} on YouTube")
    webbrowser.open("https://youtu.be/p6ca7gq5H70?si=m4gjwt5EnwPtuRF0{song}")


# ================= COMMAND HANDLER =================
def respond(voice_data):
    if 'your name' in voice_data:
        alexis_speak("My name is noah")

    elif 'time' in voice_data:
        alexis_speak(ctime())

    elif 'search' in voice_data:
        query = record_audio("What do you want to search?")
        webbrowser.open(f"https://www.google.com/search?q={query}")

    elif 'find location' in voice_data:
        place = record_audio("What location?")
        webbrowser.open(f"https://www.google.com/maps/search/?api=1&query={place}")

    elif 'weather' in voice_data or 'temperature' in voice_data:
        get_weather()

    elif 'wikipedia' in voice_data:
        topic = voice_data.replace('wikipedia', '').strip()
        webbrowser.open(f"https://www.wikipedia.org/={topic}")

    elif 'play' in voice_data:
        song = voice_data.replace('play', '').strip()
        play_song(song)



    elif 'exit' in voice_data or 'quit' in voice_data:
        alexis_speak("Goodbye sir")
        exit()

# ================= MAIN =================
time.sleep(1)
alexis_speak("hi sir! i am your voice assistant, How can I help you?")

while True:
    command = record_audio()
    respond(command)