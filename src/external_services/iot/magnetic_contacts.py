import time

from src.external_services.iot.bridge.homey import update_status, get_device_current_value
from src import sound_effects

def manget_contacts(device_data):
	devices_to_watch ={ 
		"door magnet": {
			"target_capability": "alarm_contact",
			"interval": 3
		}
	}

	threads_num = update_status(device_data, devices_to_watch)
	print(f"Monitors: {threads_num} magnets")

	while True:
		door = get_device_current_value("door magnet", "alarm_contact")
		if door:
			sound_effects.play_mp3("alarms/chinese_alarm")
		time.sleep(3)