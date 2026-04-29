import time

from src.external_services.iot.bridge.homey import update_status, get_device_current_value
from src import voice_communication, timer

def thermometers(device_data):
	devices_to_watch = {
		"thermometer": {
			"target_capability": "measure_humidity",
			"interval": 30
		}
	}
	
	threads_num = update_status(device_data, devices_to_watch)
	print(f"Monitors: {threads_num} thermometer")
	
	within_time = "7:00:00" > timer.current_time() < "22:00:00"
	open_window_buffer = False
	while True:
		humidity = get_device_current_value("thermometer", "measure_humidity")
		if humidity and humidity > 40:
			if within_time:
				voice_communication.speak("Please open the window")
			else:
				open_window_buffer = True
		elif open_window_buffer and within_time:
			voice_communication.speak("Please open the window")
			open_window_buffer = False
		time.sleep(30)