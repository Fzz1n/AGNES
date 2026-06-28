import time

from src.external_services.iot.bridge.homey import update_status, get_device_current_value
from src import voice_communication, timer
from src.external_services.iot.magnetic_contacts import should_window_be_closed

def thermometers(device_data):
	devices_to_watch = {
		"thermometer": {
			"target_capability": ["measure_temperature", "measure_humidity"],
			"interval": 30
		}
	}
	
	threads_num = update_status(device_data, devices_to_watch)
	print(f"Monitors: {threads_num} thermometer")
	
	open_window_buffer = False
	while True:
		within_time = "07:00:00" < timer.current_time() < "22:00:00"
		temp = get_device_current_value("thermometer", "measure_temperature")
		humidity = get_device_current_value("thermometer", "measure_humidity")
		
		if humidity and humidity > 40:
			window_bed_open = get_device_current_value("window sensor0", "alarm_contact")
			window_living_open = get_device_current_value("window sensor1", "alarm_contact")
			if within_time and not (window_bed_open or window_living_open or should_window_be_closed(temp)):
				voice_communication.speak("Please open the window")
			else:
				open_window_buffer = True
		elif open_window_buffer and within_time and not should_window_be_closed(temp):
			voice_communication.speak("Please open the window")
			open_window_buffer = False
		time.sleep(300)