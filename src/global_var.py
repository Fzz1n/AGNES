import threading

MONTHS = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
WEEKSDAY_NAME = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
misunderstanding_counter = 0
misunderstanding_timer = None
weather_data = None
weather_data_age = None
stop_event = threading.Event()
coordinates = None
last_answer = "No previous response"
time_left = 0