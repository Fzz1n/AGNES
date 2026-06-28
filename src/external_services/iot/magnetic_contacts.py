import os, threading
from dotenv import load_dotenv
load_dotenv()

from src.external_services.iot.bridge.homey import update_status
from src.external_services.iot.services.windows import should_window_be_closed
from src.external_services.iot.services.doors import doorbell

SEC_CODE = os.environ["secret_code"]

def manget_contacts(device_data):
	magnet_body ={
		"target_capability": ["alarm_contact"],
		"interval": 3
	}
	
	devices_to_watch = {}
	magnet_names = []
	for key, val in device_data.items():
		if magnet_body["target_capability"][0] in val["capabilities"]:
			devices_to_watch[key] = magnet_body
			room = val["room"]

			if room == "entre":
				t = threading.Thread(target = doorbell, args = (room,), daemon = True)
				t.start()
			else:
				magnet_names.append(room)

	threads_num = update_status(device_data, devices_to_watch)
	print(f"Monitors: {threads_num} magnets")
	
	for name in magnet_names:
		t = threading.Thread(
			target = should_window_be_closed, 
			args = (name,), 
			daemon = True)
		t.start()