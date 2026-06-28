import threading

from src.external_services.iot.bridge.homey import update_status, get_device_current_value, get_devices
from src.external_services.iot.services.windows import should_window_be_open

def thermometers(device_data):
	thermometer_body = {
		"target_capability": ["measure_temperature", "measure_humidity"],
		"interval": 30
	}
	
	devices_to_watch = {}
	thermometer_names = []
	for key, val in device_data.items():
		if thermometer_body["target_capability"][0] in val["capabilities"]:
			devices_to_watch[key] = thermometer_body
			thermometer_names.append(val["room"])

	threads_num = update_status(device_data, devices_to_watch)
	print(f"Monitors: {threads_num} thermometer")
	
	for name in thermometer_names:
		thread = threading.Thread(
			target = should_window_be_open,
			args = (name,),
			daemon = True
		)
		thread.start()

d = {'plug_kontor': {'id': '01c21cbc-ea7f-4856-97e8-de6dab30db51', 'room': 'kontor', 'capabilities': ['onoff', 'meter_power', 'measure_power', 'measure_voltage', 'measure_current']}, 'thermometer_living': {'id': '2fbe9c38-fd64-483a-a835-811180122d23', 'room': 'living', 'capabilities': ['measure_temperature', 'measure_humidity', 'measure_battery']}, 'door magnet_entre': {'id': '4a073083-4d76-415a-8449-46c29afaafeb', 'room': 'entre', 'capabilities': ['measure_battery', 'alarm_tamper', 'alarm_battery', 'alarm_generic', 'alarm_contact']}, 'thermometer_bedroom': {'id': '68cd9802-dd81-4c91-a503-d7f893cd4463', 'room': 'bedroom', 'capabilities': ['measure_temperature', 'measure_humidity', 'measure_battery']}, 'thermometer_wc': {'id': 'cd56a47d-de66-46b6-b204-d884dc33a27a', 'room': 'wc', 'capabilities': ['measure_temperature', 'measure_humidity', 'measure_battery']}, 'window magnet_bedroom': {'id': 'e67949b1-ec30-46b0-b102-e39f1a99796e', 'room': 'bedroom', 'capabilities': ['measure_battery', 'button.identify', 'alarm_contact']}}
#print(thermometers(d))