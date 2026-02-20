import time

from src import sound_effects
from src import converter

def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end='\r')  # Overwrite the line each second
        time.sleep(1)
        t -= 1

def start_timer(text):
    countdown(converter.get_time(text))
    sound_effects.play_mp3("alarms/classic_alarm")