import os
import platform
import subprocess
from gtts import gTTS
import speech_recognition as sr

from src import global_var, timer

# Converting text to audio
def speak(text):
    global_var.set_global_var("last_answer", text) # Saving the answer
    tts = gTTS(text=text, lang="en")
    filename = "voice.mp3"
    tts.save(filename)

    system = platform.system()

    if system == "Linux":
        subprocess.run(["mpg123", "-q", filename])
    elif system == "Windows":
        import playsound
        playsound.playsound(filename)

    os.remove(filename)

# Converting audio to text
def get_audio(r, source, lang):
    try:
        audio = r.listen(source, phrase_time_limit = 10) # addition ", timeout=10, phrase_time_limit=8"
        said = r.recognize_google(audio, language=lang) # Danish -> da-DK || English(US) -> en-US
        print("You said:", said.lower())
        return said.lower()

    except sr.WaitTimeoutError:
        print("No sound recorded")
        return
    
    except sr.UnknownValueError:
        # Auto adjust the energy threshold, if enough misunderstandings happens
        DEAFAULT_ENERGY_THRESHOLD = global_var.get_global_var("default_energy_threshold")
        global_var.misunderstanding_counter += 1
        miss_counter = global_var.misunderstanding_counter
        miss_timer = global_var.misunderstanding_timer
        time_now = timer.current_time_sec()
        
        if miss_timer is None:
            global_var.misunderstanding_timer = time_now

        # More than 20 misunderstandings and les than 5 min    
        elif miss_counter >= 20 and (time_now - miss_timer) <= 300:
            r.energy_threshold += 50
            global_var.misunderstanding_counter = 0
            global_var.misunderstanding_timer = time_now
            msg = f"Upgrading energy threshold to {r.energy_threshold}"
            print(msg)
            if not r.energy_threshold > 500:
                speak(msg)
        
        # Older whan 30 min
        elif (time_now - miss_timer) > (60 * 30):
            print("Resetting values")
            global_var.misunderstanding_counter = 0
            global_var.misunderstanding_timer = time_now
            
            # Adjust to deafault value, if 700 or below deafault value, else -100
            if (r.energy_threshold == 700) or ((r.energy_threshold - 100) < DEAFAULT_ENERGY_THRESHOLD):
                r.energy_threshold = DEAFAULT_ENERGY_THRESHOLD
            else:
                r.energy_threshold -= 100

        print(f"Couldn't understand audio {timer.current_time()}, Counter: {global_var.misunderstanding_counter}")
        return
    
    except sr.RequestError as e:
        print("Google API error:", e)
        speak("Google API error. Try again later")
        return
    
    except:
        print("Uninspected error")
        return