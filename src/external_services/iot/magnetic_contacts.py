import os
import requests
import json
import time
import threading
from dotenv import load_dotenv
load_dotenv()
import ast

from src import calc, converter, global_var, voice_communication
from src.external_services.iot.bridge.homey import get_status, get_current_value

HOMEY_KEY = os.environ["homey_key"]
HOMEY_IP_ADDRESS = os.environ["homey_ip_address"]
REST_API = f"http://{HOMEY_IP_ADDRESS}/api/manager/"

def start_monetoring():
	devices_data = global_var.get_global_var("iot_devices")
	devices_data = ast.literal_eval(devices_data)
	
	device_watch = {
		"plug": {
			"target_capability": "measure_power",
			"interval": 2
		},
		"door magnet": {
			"target_capability": "alarm_contact",
			"interval": 3
		},
		"thermometer": {
			"target_capability": "measure_humidity",
			"interval": 30
		}
	}

	threads = []
	for device_name, config in device_watch.items():
		device_id = devices_data[device_name]["id"]
		url = REST_API + f"devices/device/{device_id}"

		thread = threading.Thread(
			target = get_status,
			args = (url, device_name, config["target_capability"], config["interval"]),
			daemon = True
		)
		thread.start()
		threads.append(thread)

	print(f"Monitors {len(threads)} devices")

from src import sound_effects
if __name__ == "__main__":
	thread = threading.Thread(
			target = start_monetoring,
			args = (),
			daemon = True
		)
	thread.start()

	try:
		while True:
			door = get_current_value("door magnet", "alarm_contact")
			if door:
				sound_effects.play_mp3("alarms/chinese_alarm")
			time.sleep(3)
	except KeyboardInterrupt:
		print("Stopping the program...")

#python -m src.external_services.iot.magnetic_contacts