import threading

stop_event = threading.Event()
misunderstanding_counter = 0
weeks_day_name = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
weeks_day_name_int = {"monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3, "friday": 4, "saturday":5 , "sunday": 6}
coordinates = None
weather_data = None
weather_data_age = None
last_answer = "No previous response"
months = {"january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6, "july": 7, "august": 8, "september": 9, "october": 10, "november": 11, "december": 12}
time_left = 0