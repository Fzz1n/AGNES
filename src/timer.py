import time
import datetime
import threading

import src.global_var
from src import sound_effects
from src import converter

def countdown(t):
    while t and not src.global_var.stop_event.is_set():
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end='\r')  # Overwrite the line each second
        time.sleep(1)
        t -= 1
    if not src.global_var.stop_event.is_set():
        sound_effects.play_mp3("alarms/classic_alarm")
    else:
        print("Alarm stoped")

def start_timer(text):
    countdown(converter.get_time(text))

# Get now time in sec
def current_time_sec():
    return time.time()

# Get current time
def current_time():
    return time.strftime("%X")

# Get todays date
def todays_date():
    return time.strftime("%x")

# Get todays weekday name
def todays_weekday_name(days_ahead = 0):
    return (datetime.date.today() + datetime.timedelta(days=days_ahead)).strftime('%A')

# Get current month
def current_month_name():
    return time.strftime("%B")

# Get this week number
def current_week_number():
    return time.strftime("%V")

# Get teh next date based on a week day name
def next_date_by_weekday(target_weekday: int):
    today = datetime.date.today()
    today_weekday = today.weekday()  # 0=Mon, 6=Sun
    
    days_ahead = (target_weekday - today_weekday) % 7
    if days_ahead == 0:
        days_ahead = 7 
    
    return today + datetime.timedelta(days=days_ahead)

# Compare old current time in sec
def older_than_7_days(start_time):
    if start_time is None:
        return True
    diff_sec = current_time_sec() - start_time
    diff_days = diff_sec / (60 * 60 * 24)
    
    # Max 7 days old
    return diff_days > 7
