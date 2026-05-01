import os, time, threading
from dotenv import load_dotenv
load_dotenv()

from src.external_services.iot.bridge.homey import update_status, get_device_current_value, get_status
from src import sound_effects, voice_communication, global_var

SEC_CODE = os.environ["secret_code"]

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
			sound_effects.play_mp3_with_custom_volume("alarms/chinese_alarm", 50)
		time.sleep(3)

def door_alarm():
	time.sleep(300)
	while True:
		door = get_device_current_value("door magnet", "alarm_contact")
		if door:
			stop_event = threading.Event()
			t = threading.Thread(target=alarm_countdown, args=(stop_event,), daemon = True)
			t.start()

			while True:
				try:
					res = global_var.audio_queue.get(timeout=1)
					if res == SEC_CODE:
						break

				except:
					pass
			
			stop_event.set()
			global_var.save_audio.clear()
			try:
				while True:
					global_var.audio_queue.get_nowait()
			except:
				pass
			break
		time.sleep(3)

def alarm_countdown(stop):
	voice_communication.speak("The alarm will go off in 30 sec.")
	
	# 30 sec. countdown, stops if the event (stop) ends
	for sec in range(30):
		if stop.is_set():
			voice_communication.speak("Alarm stopped")
			return
		time.sleep(1)
	
	# Alarm goes off
	while not stop.is_set():
		sound_effects.play_mp3("alarms/danger_alarm")