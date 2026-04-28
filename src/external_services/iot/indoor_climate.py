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
	
	time_limit = "7:00:00" > timer.current_time() < "22:00:00"
	while True:
		humidity = get_device_current_value("thermometer", "measure_humidity")
		if humidity and humidity > 40 and time_limit:
			voice_communication.speak("Please open the window")
		time.sleep(30)