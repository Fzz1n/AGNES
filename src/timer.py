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

# Get current time
def current_time():
    return time.strftime("%X")

# Get todays date
def todays_date():
    return time.strftime("%x")

# Get todays weekday name
def todays_weekday_name():
    return time.strftime("%A")

# Get current month
def current_month_name():
    return time.strftime("%B")

# Get this week number
def current_week_number():
    return time.strftime("%V")