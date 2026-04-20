import os
import platform
import subprocess
import audioop
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
def get_audio(r, source, lang, ET_deafault):
    try:
        audio = r.listen(source, phrase_time_limit = 10) # addition ", timeout=10, phrase_time_limit=8"
        
        # Calc. the energy threshold from audio
        data = audio.frame_data
        ET_live = audioop.rms(data, 2)
        change_ET = None
        print(f"ET_live {ET_live}")
        
        # Set energy threshold to 400 to avoid unassesary noize
        if global_var.misunderstanding_counter >= 10:
            change_ET = 400

            miss_timer = global_var.misunderstanding_timer
            time_now = timer.current_time_sec()
            if miss_timer is None:
                global_var.misunderstanding_timer = time_now
            
            # More than 5 min. has past
            if (time_now - miss_timer) >= 300:
                global_var.misunderstanding_counter = 0
                global_var.misunderstanding_timer = time_now
            else:
                print(f"Speak up, dafault ET are: {ET_deafault}")
        
        MAX = ET_deafault * 3
        MIN = change_ET if change_ET else ET_deafault * 0.8
        # Check energy threshold of recording
        if ET_live > MAX or ET_live < MIN:
            print("Ignore command")
            global_var.misunderstanding_counter += 1
            return
        
        said = r.recognize_google(audio, language=lang) # Danish -> da-DK || English(US) -> en-US
        print("You said:", said.lower())
        return said.lower()

    except sr.WaitTimeoutError:
        print("No sound recorded")
        return
    
    except sr.UnknownValueError:
        global_var.misunderstanding_counter += 1
        print(f"Couldn't understand audio {timer.current_time()}, Counter: {global_var.misunderstanding_counter}")
        return
    
    except sr.RequestError as e:
        print("Google API error:", e)
        return
    
    except Exception as e:
        print("Uninspected error:", e)
        return