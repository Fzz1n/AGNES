import time
from src.external_services.iot.bridge.homey import get_device_current_value
from src import voice_communication, global_var, timer

def should_window_be_open(room):
	open_window_buffer = False
	while True:
		within_time = "07:00:00" < timer.current_time() < "22:00:00"
		temp = get_device_current_value(f"thermometer_{room}", "measure_temperature")
		humidity = get_device_current_value(f"thermometer_{room}", "measure_humidity")
		
		if humidity and humidity > 40:
			window_open = get_device_current_value(f"window magnet_{room}", "alarm_contact")
			if within_time and not (window_open or weather_vs_indoor_climate(temp)):
				voice_communication.speak(f"Please open the {room} window")
			else:
				open_window_buffer = True
		elif open_window_buffer and within_time and not weather_vs_indoor_climate(temp):
			voice_communication.speak(f"Please open the {room} window")
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
				window_open = get_device_current_value(F"window magnet_{room}", "alarm_contact")
				data_exist = temp and humidity
				
				if weather_vs_indoor_climate(temp) or (data_exist and (temp < 18 or humidity < 40 and temp < 23)):
					voice_communication.speak(f"Please close the {room} window")
				time.sleep(250)

		elif not window_open and window_already_open:
			window_already_open = True
		
		time.sleep(3)

def weather_vs_indoor_climate(indoor_temp):
	if not indoor_temp:
		return True
	
	temp = global_var.current_weather.get("temp",0) > indoor_temp
	wind = global_var.current_weather.get("wind",0) > 25
	humidity = global_var.current_weather.get("humidity",0) > 80
	precipitation = global_var.current_weather.get("precipitation",1) > 0
	rain = global_var.current_weather.get("rain",1) > 0
	snow = global_var.current_weather.get("snow",1) > 0
	
	return temp or wind or humidity or precipitation or rain or snow