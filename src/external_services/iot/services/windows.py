import time
from src.external_services.iot.bridge.homey import get_device_current_value
from src import voice_communication, global_var, timer

def should_window_be_open(room):
	open_window_buffer = False
	open_window_counter = 0
	while True:
		within_time = "07:00:00" < timer.current_time() < "22:00:00"
		temp = get_device_current_value(f"thermometer_{room}", "measure_temperature")
		humidity = get_device_current_value(f"thermometer_{room}", "measure_humidity")
		weather_ok = weather_allows_the_window_to_be_open(temp)
		can_notify = within_time and open_window_counter < 2

		def notify():
			target_room = room if "room" in room else room + " room"
			voice_communication.speak(f"Please open the {target_room} window")

		if humidity is not None and humidity > 40:
			is_window_open = get_device_current_value(f"window magnet_{room}", "alarm_contact")
			if is_window_open:
				open_window_counter = 0
			elif weather_ok and is_window_open is not None:
				if can_notify:
					notify()
					open_window_counter += 1
				else:
					open_window_buffer = True
		elif open_window_buffer and weather_ok and can_notify and is_window_open is not None:
			notify()
			open_window_counter += 1
			open_window_buffer = False
		time.sleep(300)
		
def should_window_be_closed(room):
	window_already_open = False
	while True:
		window_open = get_device_current_value(F"window magnet_{room}", "alarm_contact")
		
		if window_open and not window_already_open:
			window_already_open = True
			
			while window_open:
				temp = get_device_current_value(f"thermometer_{room}", "measure_temperature")
				humidity = get_device_current_value(f"thermometer_{room}", "measure_humidity")
				data_exist = temp is not None and humidity is not None
				
				if not weather_allows_the_window_to_be_open(temp) or (data_exist and (temp < 18 or humidity < 40 and temp < 23)):
					target_room = room if "room" in room else room + " room"
					voice_communication.speak(f"Please close the {target_room} window")
				time.sleep(240)
				window_open = get_device_current_value(F"window magnet_{room}", "alarm_contact")

		elif not window_open and window_already_open:
			window_already_open = False
		
		time.sleep(3)

def weather_allows_the_window_to_be_open(indoor_temp):
	if not indoor_temp:
		return False
	
	temp = global_var.current_weather.get("temp",20) < indoor_temp			# Hotter indoor vs outdoor
	wind = global_var.current_weather.get("wind",5) < 25					# A wind speed below 25 m/s
	humidity = global_var.current_weather.get("humidity",50) < 80			# Humidity outside below 80%
	precipitation = global_var.current_weather.get("precipitation",0) == 0	# 0 mm of precipitation
	rain = global_var.current_weather.get("rain",0) == 0					# 0 mm of rain
	snow = global_var.current_weather.get("snow",0) == 0					# 0 mm of snow
	
	return temp and wind and humidity and precipitation and rain and snow