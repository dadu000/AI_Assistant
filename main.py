import datetime
import os
import sys
import time
import webbrowser
import pyautogui
#import pyttsx3
import speech_recognition as sr
import json
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import random
import numpy as np
import psutil
import requests
from elevenlabs.client import ElevenLabs
from elevenlabs import play
import wikipedia
from api_key import Voce_api_key, NEWS_API_KEY ,WEATHER_API_KEY # Import both keys from api_key.py
import pygame.mixer

# Initialize ElevenLabs client with API key
client = ElevenLabs(api_key=Voce_api_key)

# News fetching function
def fetch_news(topic="general"):
    """Fetch news from NewsAPI using the API key stored in api_key.py."""
    url = f"https://newsapi.org/v2/top-headlines?category={topic}&apiKey={NEWS_API_KEY}"
    try:
        response = requests.get(url).json()
        if response['status'] == "ok":
            articles = response['articles'][:3]  # Top 3 headlines
            news = f"Here’s the latest {topic} news: "
            for i, article in enumerate(articles, 1):
                news += f"{i}. {article['title']} from {article['source']['name']}. "
            return news
        return "Sorry, I couldn’t fetch the news right now."
    except Exception as e:
        return f"Error fetching news: {str(e)}"


def fetch_weather(location):
    """Fetch weather from OpenWeatherMap using the API key stored in api_key.py."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={WEATHER_API_KEY}&units=metric"
    try:
        response = requests.get(url).json()
        if response['cod'] == 200:  # Success status code
            weather = response['weather'][0]['description']
            temp = response['main']['temp']
            feels_like = response['main']['feels_like']
            return (f"The weather in {location} is {weather}. "
                    f"The temperature is {temp} degrees Celsius, and it feels like {feels_like} degrees Celsius.")
        return f"Sorry, I couldn’t fetch the weather for {location}. Please check the location name."
    except Exception as e:
        return f"Error fetching weather: {str(e)}"
    
def engine_talk(query):
    audio_generator = client.generate(
        text=query,
        voice='Grace',
        model="eleven_monolingual_v1"
    )
    audio_bytes = b''.join(audio_generator)
    file_path = os.path.abspath("temp_audio.mp3")
    with open(file_path, "wb") as f:
        f.write(audio_bytes)
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
    pygame.mixer.quit()
    os.remove(file_path)

with open("intents.json") as file:
    data = json.load(file)

model = load_model("chat_model.h5")
with open("tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)
with open("label_encoder.pkl", "rb") as encoder_file:
    label_encoder = pickle.load(encoder_file)


# use if you don't have ElevenLabs API key
# def initialize_engine():
#     engine = pyttsx3.init("sapi5")
#     voices = engine.getProperty('voices')
#     engine.setProperty('voice', voices[1].id)
#     rate = engine.getProperty('rate')
#     engine.setProperty('rate', rate-50)
#     volume = engine.getProperty('volume')
#     engine.setProperty('volume', volume+0.25)
#     return engine

# def speak(text):
#     engine = initialize_engine()
#     engine.say(text)
#     engine.runAndWait()

def command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening.......", end="", flush=True)
        r.pause_threshold = 1.0
        audio = r.listen(source)
    try:
        print("\r", end="", flush=True)
        print("Recognizing......", end="", flush=True)
        query = r.recognize_google(audio, language='en-in')
        print(f"User said : {query}\n")
    except Exception:
        print("Say that again please")
        return "None"
    return query

def cal_day():
    day = datetime.datetime.today().weekday() + 1
    day_dict = {
        1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday",
        5: "Friday", 6: "Saturday", 7: "Sunday"
    }
    return day_dict.get(day, "Unknown")

def data_and_time():
    hour = int(datetime.datetime.now().hour)
    t = time.strftime("%I:%M:%p")
    day = cal_day()
    if 0 <= hour <= 12 and 'AM' in t:
        engine_talk(f"it's {day} and the time is {t}")
    elif 12 <= hour <= 16 and 'PM' in t:
        engine_talk(f"it's {day} and the time is {t}")
    else:
        engine_talk(f"it's {day} and the time is {t}")

def social_media(command):
    sites = {
        'facebook': "https://www.facebook.com/",
        'whatsapp': "https://web.whatsapp.com/",
        'discord': "https://discord.com/",
        'instagram': "https://www.instagram.com/"
    }
    for site, url in sites.items():
        if site in command:
            engine_talk(f"opening your {site}")
            webbrowser.open(url)
            return
    engine_talk("No result found")

def schedule():
    day = cal_day().lower()
    engine_talk("Boss today's schedule is ")
    week = {
        "monday": "Boss, from 9:00 to 9:50 you have Algorithms class, from 10:00 to 11:50 you have System Design class, from 12:00 to 2:00 you have a break, and today you have Programming Lab from 2:00 onwards.",
        "tuesday": "Boss, from 9:00 to 9:50 you have Web Development class, from 10:00 to 10:50 you have a break, from 11:00 to 12:50 you have Database Systems class, from 1:00 to 2:00 you have a break, and today you have Open Source Projects lab from 2:00 onwards.",
        "wednesday": "Boss, today you have a full day of classes. From 9:00 to 10:50 you have Machine Learning class, from 11:00 to 11:50 you have Operating Systems class, from 12:00 to 12:50 you have Ethics in Technology class, from 1:00 to 2:00 you have a break, and today you have Software Engineering workshop from 2:00 onwards.",
        "thursday": "Boss, today you have a full day of classes. From 9:00 to 10:50 you have Computer Networks class, from 11:00 to 12:50 you have Cloud Computing class, from 1:00 to 2:00 you have a break, and today you have Cybersecurity lab from 2:00 onwards.",
        "friday": "Boss, today you have a full day of classes. From 9:00 to 9:50 you have Artificial Intelligence class, from 10:00 to 10:50 you have Advanced Programming class, from 11:00 to 12:50 you have UI/UX Design class, from 1:00 to 2:00 you have a break, and today you have Capstone Project work from 2:00 onwards.",
        "saturday": "Boss, today you have a more relaxed day. From 9:00 to 11:50 you have team meetings for your Capstone Project, from 12:00 to 12:50 you have Innovation and Entrepreneurship class, from 1:00 to 2:00 you have a break, and today you have extra time to work on personal development and coding practice from 2:00 onwards.",
        "sunday": "Boss, today is a holiday, but keep an eye on upcoming deadlines and use this time to catch up on any reading or project work."
    }
    if day in week:
        engine_talk(week[day])

def openApp(command):
    apps = {'calculator': 'calc.exe', 'notepad': 'notepad.exe', 'paint': 'mspaint.exe'}
    for app, exe in apps.items():
        if app in command:
            engine_talk(f"opening {app}")
            os.startfile(f'C:\\Windows\\System32\\{exe}')
            return

def closeApp(command):
    apps = {'calculator': 'calc.exe', 'notepad': 'notepad.exe', 'paint': 'mspaint.exe'}
    for app, exe in apps.items():
        if app in command:
            engine_talk(f"closing {app}")
            os.system(f"taskkill /f /im {exe}")
            return

def browsing(query):
    if 'google' in query:
        engine_talk("Boss, what should I search on google?")
        s = command().lower()
        webbrowser.open(f"https://www.google.com/search?q={s}")

def condition():
    usage = psutil.cpu_percent()
    battery = psutil.sensors_battery()
    percentage = battery.percent if battery else 100
    engine_talk(f"CPU is at {usage} percentage. Boss our system has {percentage} percentage battery")
    if percentage >= 80:
        engine_talk("Boss we have enough charge to continue")
    elif 40 <= percentage <= 75:
        engine_talk("Boss we should plug in soon")
    else:
        engine_talk("Boss we’re low on power, please charge now!")



def wikipedia_search(query):
    """Fetch a summary from Wikipedia based on the query."""
    try:
        if "wikipedia" in query:
            topic = query.split("wikipedia")[-1].strip()
        elif "tell me about" in query:
            topic = query.split("tell me about")[-1].strip()
        else:
            topic = query.strip()
        summary = wikipedia.summary(topic, sentences=2)
        return f"Here’s what I found on Wikipedia about {topic}: {summary}"
    except wikipedia.exceptions.DisambiguationError:
        return "There are multiple results for that topic. Please be more specific."
    except wikipedia.exceptions.PageError:
        return "Sorry, I couldn’t find anything on Wikipedia about that."
    except Exception as e:
        return f"Error fetching Wikipedia info: {str(e)}"

if __name__ == "__main__":
    # wishMe()
    engine_talk("Allow me to introduce myself, I am Iris, your virtual AI assistant here to help!")
    while True:
        query = command().lower()
        if query == "none":
            continue

        elif any(x in query for x in ["tell me the  date", "tell me the time", "time me the data and time", " waht was the time " ,"what is the date and time",]):
           data_and_time()
        elif any(x in query for x in ["facebook", "discord", "whatsapp", "instagram"]):
            social_media(query)
        elif "schedule" in query or " time table" in query:
            schedule()
        elif "volume up" in query or "increase volume" in query:
            pyautogui.press("volumeup")
            engine_talk("Volume increased")
        elif "volume down" in query or "decrease volume" in query:
            pyautogui.press("volumedown")
            engine_talk("Volume decreased")
        elif "volume mute" in query or "mute the sound" in query or "mute the volume" in query:
            engine_talk("Volume muted")
            pyautogui.press("volumemute")

        elif "unmute" in query or "volume unmute" in query or "unmute the volume" in query:
            pyautogui.press("volumemute")
            engine_talk("Volume unmuted")   
            
        elif "open" in query and any(x in query for x in ["calculator", "notepad", "paint"]):
            openApp(query)
        elif "close" in query and any(x in query for x in ["calculator", "notepad", "paint"]):
            closeApp(query)
        elif "google" in query:
            browsing(query)
        elif "system condition" in query:
            condition()
        elif "news" in query:
            topic = "sports" if "sports" in query else "general"
            news = fetch_news(topic)
            engine_talk(news)
        elif any(x in query for x in ["wikipedia", "tell me about", "what is", "who is", "explain", "info on", "describe","today news"]):
                result = wikipedia_search(query)
                engine_talk(result)
        elif "exit" in query:
            sys.exit()
        else:
            padded_sequences = pad_sequences(tokenizer.texts_to_sequences([query]), maxlen=20, truncating='post')
            result = model.predict(padded_sequences)
            tag = label_encoder.inverse_transform([np.argmax(result)])[0]
            for i in data['intents']:
                if i['tag'] == tag:
                    response = np.random.choice(i['responses'])
                    engine_talk(response)
                    break