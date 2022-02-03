from ensurepip import version
from subprocess import call
from unittest import mock
from urllib.request import DataHandler
import pydub
import speech_recognition as sr
from time import ctime
import webbrowser
import time
import os
import random
import gtts
from pydub import AudioSegment
from pydub.playback import play
import python_weather
import asyncio
import shelve

r = sr.Recognizer()
pydub.AudioSegment.ffmpeg = "C:/FFmpeg"
questions = ['Quelle heure est-il?', 'Quel jour est-ce aujourd\'hui?', 'Quelle est la date?', 'Quel est le mois?', 'Quand est ton anniversaire?', 'Quel âge as-tu?', 'Quel âge a ton grand-père?', 'Comment t\'appelles-tu?', 'Comment s\'appelle ton prof de maths?', 'Comment vas-tu?', 'Quand tu as faim, qu\'est-ce que tu aimes manger?', 'Quand tu as soif, qu\'est-ce que tu aimes boire?', 'Combien coûte le livre de français?', 'Est-ce que tu vas jouer au basket aujourd\'hui?', 'Tu aimes téléphoner?', 'Tu aimes parler français?', 'Où es-tu maintenant?', 'Tes parents sont en vacances?', 'Où habites-tu?', 'Avec qui parles-tu français?',
             'Tu es français(e)?', 'A quelle heure est-ce que tu étudies?', 'Comment est-ce que tu chantes?', 'Comment est-ce que tu nages?', 'Voyagez-vous souvent?', 'Qui est-ce que tu invites au cinéma?', 'Comment s\'appelle ton meilleur', 'Comment s\'appelle ton ami?', 'Tu as une guitare?', 'De quelle couleur est la voiture de ton père?', 'Es-tu une personne intelligente, sincère, et sympathique?', 'Avec qui étudies-tu?', 'Aimez-vous chanter?', 'Quel sport aimes-tu jouer?', 'A quelle heure est-ce que vous dînez?', 'Tu préfères écouter la musique classique, le rock, ou le rap?', 'De quelle couleur préfères-tu?', 'Tu n\'aimes pas la couleur bleue?', 'Est-ce que c\'est vrai que Miami est en Californie?', 'Quel jour aimes-tu?', 'Quel restaurant est-ce que tu aimes?']


class main():
    location = ''
    called = False
    frenchMode = False
    pracFrenchMode = False
    shelf = shelve.open("var.dat")
    location = shelf['location']
    shelf.close()


def record(ask=False):
    with sr.Microphone() as source:
        if(ask):
            speak(ask)
        audio = r.listen(source)
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio)
        except sr.UnknownValueError:
            if(main.called):
                speak('sorry I didn\'t get that')
        except sr.RequestError:
            if(main.called):
                speak('sorry, im down right now')
        return voice_data


def speak(audio_string):
    if(main.frenchMode):
        francaisSpeak(audio_string)
    elif(main.frenchMode == False):
        Engspeak(audio_string)


def Engspeak(audio_string):
    tts = gtts.gTTS(text=audio_string, lang='en')
    re = random.randint(1, 100000000)
    audio_file = "audio" + str(re) + ".mp3"
    tts.save(audio_file)
    sound = AudioSegment.from_file(audio_file)
    play(sound)
    print(audio_string)
    os.remove(audio_file)


def francaisSpeak(audio_string):
    tts = gtts.gTTS(text=audio_string, lang='fr')
    re = random.randint(1, 100000000)
    audio_file = "audio" + str(re) + ".mp3"
    tts.save(audio_file)
    sound = AudioSegment.from_file(audio_file)
    play(sound)
    print(audio_string)
    os.remove(audio_file)


def pracFrench():
    rand = 0
    while(main.pracFrenchMode == True):
        rand = random.randint(0, 39)
        speak(questions[rand])
        time.sleep(5)


def respond(voice_data):
    if(main.pracFrenchMode == False):
        if('name' in voice_data):
            speak('My name is bob')
        if('time' in voice_data):
            speak(ctime())
        if('search' in voice_data and 'for' not in voice_data):
            search = record('What do you want to search for?')
            if(search != ''):
                url = 'https://google.com/search?q=' + search
                webbrowser.get().open(url)
                speak('Here is what I found for: ' + search)
        if('search for' in voice_data):
            search = record()
            if(search != ''):
                url = 'https://google.com/search?q=' + search
                webbrowser.get().open(url)
                speak('Here is what I found for: ' + search)
        if('location' in voice_data and 'find' in voice_data):
            location = record('What is the location?')
            if(location != ''):
                url = 'https://google.nl/maps/place/' + location + '/&amp;'
                webbrowser.get().open(url)
                speak('Here is what I found for: ' + location)
        if('find' in voice_data and 'location' not in voice_data):
            location = record()
            if(location != ''):
                url = 'https://google.nl/maps/place/' + location + '/&amp;'
                webbrowser.get().open(url)
                speak('Here is what I found for: ' + location)
        if('weather' in voice_data and 'today' in voice_data):
            loop = asyncio.get_event_loop()
            loop.run_until_complete(getWeather(main.location, 1))
        if('weather' in voice_data and 'next' in voice_data):
            days = record('how many days do you want the weather for?')
            if(int(days) > 4):
                speak('Im sorry, I can only predict up to 4 days, I will do that now')
                loop.run_until_complete(getWeather(main.location, int(4)))
            elif(int(days) > 0):
                loop.run_until_complete(getWeather(main.location, int(days)))
            else:
                speak('Im sorry, I can\'t get the weather for past days')
            loop = asyncio.get_event_loop()

        if('deactivate' in voice_data):
            speak('deactivating, say hello for re-activation')
            main.called = False
        if('exit program' in voice_data):
            speak('exiting program...')
            main.called = False
            shelf2 = shelve.open('C:/Users/ravip/Desktop\BOB/var')
            shelf2['location'] = main.location
            shelf2.close()
            exit()
        if('location' in voice_data and 'set' in voice_data):
            locat = record('The current location is ' +
                           main.location + ', what is the new location?')
            if(locat != ''):
                main.location = locat
                shelf2 = shelve.open('var.dat')
                shelf2['location'] = locat
                shelf2.close()
                speak('location set!')
        if('play' in voice_data and 'song' in voice_data):
            song = record('What song would you like to search for?')
            if(song != ''):
                words = []
                words = song.split()
                print(words)
                urlList = []
                urlList.append('https://open.spotify.com/search/')
                y = 0
                for x in words:
                    urlList.append(words[y])
                    y += 1
                url = "%20".join(urlList)
                webbrowser.get().open(url)
                speak('Here is what I found for: ' + song)
        if('activate' in voice_data and 'French' in voice_data and 'mode' in voice_data):
            main.frenchMode = True
            speak('mode français activé')
        if('deactive' in voice_data and 'French' in voice_data and 'mode' in voice_data):
            main.frenchMode = False
            speak('french mode deactivated')
        if('practice' in voice_data and 'listening' in voice_data and 'French' in voice_data):
            main.pracFrenchMode = True
            speak('I will ask you some questions in french, try and see if you can understand them! You will have 5 seconds for each question. When you want to stop practicing, say "Stop now"')
            pracFrench()
    if(main.pracFrenchMode == True and 'stop' in voice_data and 'now' in voice_data):
        main.pracFrenchMode == False


async def getWeather(location, days):
    client = python_weather.Client()
    weather = await client.find(location)
    for x in range(days):
        if(x == 1):
            speak('The temprature today is ' + str(weather.forecasts[x].temperature) +
                  ' degrees celsius and the sky is ' + str(weather.forecasts[x].sky_text))
        else:
            speak('The temprature on ' + str(weather.forecasts[x]) + 'is ' + str(
                weather.forecasts[x].temperature) + ' degrees celsius and the sky is ' + str(weather.forecasts[x].sky_text))
    await client.close()


time.sleep(1)
while True:
    voice_data = record()
    print(voice_data)
    if('hello' in voice_data and main.called == False):
        speak('How can I help you?')
        print('hello')
        main.called = True
    if(main.called == True):
        respond(voice_data)
