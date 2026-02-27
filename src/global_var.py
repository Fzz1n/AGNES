import threading

stop_event = threading.Event()
misunderstanding_counter = 0
weeks_day_name = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
coordinates = None
weather_data = None
weather_data_age = None
last_answer = "No previous response"