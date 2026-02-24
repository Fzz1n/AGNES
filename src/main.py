import os
import time
import threading
import playsound
from gtts import gTTS
import speech_recognition as sr

from src import sound_effects
from src import calc
from src import converter
from src import timer
from src.IoT import light 

def speak(text):
    tts = gTTS(text=text, lang="en")
    filename = "voice.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove("voice.mp3")

def get_audio(r, source, lang):
    while True:
        try:
            audio = r.listen(source, phrase_time_limit=8)
            said = r.recognize_google(audio, language=lang) # Danish -> da-DK || English(US) -> en-US
            print("You said:", said.lower())
            return said.lower()

        except sr.WaitTimeoutError:
            print("Ingen lyd registreret")
            continue
        
        except sr.UnknownValueError:
            print("Couldn't understand audio")
            continue
        
        except sr.RequestError as e:
            print("Google API fejl:", e)

def main():
    r = sr.Recognizer()
    r.dynamic_energy_threshold = False
    r.energy_threshold = 200
    r.listen
    
    with sr.Microphone() as source:
        print("Energy threshold:", r.energy_threshold)
        
        while True:    
            text = get_audio(r, source, "en-US")

            if "69" in text:
                sound_effects.play_mp3("nice_meme")
            
            if "hello" in text:
                speak("hello, how are you?")
            elif "what's your name" in text:
                speak("My name is AGNES")
            elif "what does agnes stand for" in text:
                speak("It stands for: Artificial Generative Nested Environment System")
            elif "energy threshold" in text:
                if "change" in text:
                    number = converter.get_number(text)
                    r.energy_threshold = number
                    speak(f"energy threshold is now changed to: {number}")
                elif "reading" in text:
                    speak(f"{round(r.energy_threshold, 2)}")
                elif "deactivate dynamic" in text:
                    r.dynamic_energy_threshold = False
                    r.energy_threshold = 200
                    speak("dynamic energy threshold is now deactivated")
                elif "activate dynamic" in text:
                    r.dynamic_energy_threshold = True
                    speak("dynamic energy threshold is now activated")
            elif "deactivate microphone" in text:
                speak("copy that")
                timer.start_timer(text)
                speak("I'm back bitches!!")
            elif "timer" in text:
                t = threading.Thread(target=timer.start_timer, args=(text,))
                t.start()
            elif "rice" in text:
                speak(f"{calc.water_to_rice(converter.get_number_and_unit(text))}")
            elif "what" in text:
                if "time" in text:
                    speak(timer.current_time())
                elif "todays date" in text:
                    speak(timer.todays_date())
                elif "day is it today" in text:
                    speak(timer.todays_weekday_name())
                elif "month" in text:
                    speak(timer.current_month_name())
                elif "week" in text:
                    speak(timer.current_week_number())
            elif "play" in text:
                if "obi-wan" in text:
                    sound_effects.play_mp3("Obi-Wan")
                elif "game" in text:
                    sound_effects.play_mp3("game_on")
            elif "adjust" in text:
                if "sound" in text:
                    sound_effects.adjust_sound(converter.get_number(text))
            elif "light" in text or "ture" in text or "going to bed" in text:
                light.controlling_lights(text)
            elif "exit" in text:
                print("Exiting program...")
                break
main()