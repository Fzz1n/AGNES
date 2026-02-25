import os
import playsound
from gtts import gTTS
import speech_recognition as sr

import src.global_var

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
            print("No sound recorded")
            continue
        
        except sr.UnknownValueError:
            src.global_var.misunderstanding_counter += 1
            print("Couldn't understand audio")
            continue
        
        except sr.RequestError as e:
            print("Google API error:", e)