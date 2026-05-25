import os, time, threading
from dotenv import load_dotenv
load_dotenv()

from src.external_services.iot.bridge.homey import update_status, get_device_current_value, get_status
from src import sound_effects, voice_communication, global_var

SEC_CODE = os.environ["secret_code"]

def manget_contacts(device_data):
	devices_to_watch ={ 
		"door magnet": {
			"target_capability": ["alarm_contact"],
			"interval": 3
		},
		"window sensor0": {
			"target_capability": ["alarm_contact"],
			"interval": 3
		},
		"window sensor1": {
			"target_capability": ["alarm_contact"],
			"interval": 3
		}
	}

	threads_num = update_status(device_data, devices_to_watch)
	print(f"Monitors: {threads_num} magnets")
	already_bedroom_window_open = False
	already_livingroom_window_open = False
	while True:
		door_open = get_device_current_value("door magnet", "alarm_contact")
		window_bed_open = get_device_current_value("window sensor0", "alarm_contact")
		window_living_open = get_device_current_value("window sensor1", "alarm_contact")

		if door_open:
			global_var.pause_audio.set()
			sound_effects.play_mp3_with_custom_volume("alarms/chinese_alarm", 50)
			global_var.pause_audio.clear()
		
		if window_bed_open and not already_bedroom_window_open:
			already_bedroom_window_open = True
			window_bed_closed = threading.Event()
			t = threading.Thread(target=watch_open_window, args=("bedroom", window_bed_closed,), daemon = True)
			t.start()
		elif not window_bed_open and already_bedroom_window_open:
			already_bedroom_window_open = True
			if window_bed_closed:
				window_bed_closed.set()

		if window_living_open and not already_livingroom_window_open:
			already_livingroom_window_open = True
			window_living_closed = threading.Event()
			t = threading.Thread(target=watch_open_window, args=("livingroom", window_living_closed,), daemon = True)
			t.start()
		elif not window_living_open and already_livingroom_window_open:
			already_livingroom_window_open = True
			if window_living_closed:
				window_living_closed.set()

		time.sleep(3)

def watch_open_window(room, open):
	while not open.is_set():
		temp = get_device_current_value("thermometer", "measure_temperature")
		humidity = get_device_current_value("thermometer", "measure_humidity")
		data_exist = temp and humidity
		if data_exist and (temp < 18 or humidity < 40 and temp < 23):
			voice_communication.speak(f"Please close the {room} window")
		time.sleep(240)

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