import time
import datetime
import threading

from src import global_var, sound_effects, converter

def countdown(t):
    while t and not global_var.stop_event.is_set():
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end='\r')  # Overwrite the line each second
        time.sleep(1)
        t -= 1
        global_var.time_left = t
    if not global_var.stop_event.is_set():
        sound_effects.play_mp3("alarms/classic_alarm")

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
    return datetime.date.today().strftime("%d-%m-%Y")

# Get todays weekday name
def todays_weekday_name(days_ahead = 0):
    return (datetime.date.today() + datetime.timedelta(days=days_ahead)).strftime('%A')

# Get current month
def current_month_name():
    return time.strftime("%B")

# Get this week number
def current_week_number(weeks_ahead = 0):
    return (datetime.date.today() + datetime.timedelta(weeks=weeks_ahead)).strftime('%V')

# Get current year
def current_year():
    return time.strftime("%Y")

# Get the next date based on a week day name
def next_date_by_weekday(target_weekday: int):
    today = datetime.date.today()
    today_weekday = today.weekday()  # 0=Mon, 6=Sun
    
    days_ahead = (target_weekday - today_weekday) % 7
    if days_ahead == 0:
        days_ahead = 7 
    
    return today + datetime.timedelta(days=days_ahead)

# Compare old current time in sec
def older_than_x_days(start_time, max_age):
    if start_time is None:
        return True
    diff_sec = current_time_sec() - start_time
    diff_days = diff_sec / (60 * 60 * 24)
    
    # Max x days old
    return diff_days > max_age

# Get start- and end-date of a week, by year and week number
def get_date_range_from_week(p_year,p_week):
    first_day_of_week = datetime.datetime.strptime(f'{p_year}-W{int(p_week )- 1}-1', "%Y-W%W-%w").date()
    last_day_of_week = first_day_of_week + datetime.timedelta(days=6.9)
    return first_day_of_week.strftime("%d-%m-%Y"), last_day_of_week.strftime("%d-%m-%Y")