import os
import requests
import json
import time
from dotenv import load_dotenv
load_dotenv()
import ast

from src import calc, converter, global_var, voice_communication
from src.external_services.iot.bridge.homey import get_devices

HOMEY_KEY = os.environ["homey_key"]
HOMEY_IP_ADDRESS = os.environ["homey_ip_address"]
REST_API = f"http://{HOMEY_IP_ADDRESS}/api/manager/"

def get_status(url):
	try:
		headers = {"Authorization": f"Bearer {HOMEY_KEY}"}
		r = requests.get(url, headers=headers, timeout=5)
	except:
		print("GET error. Try again later")
	else:
		# Find the value
		response = r.json()
		#print(response)
		value = response.get("capabilitiesObj", {}).get("alarm_contact", {}).get("value")
		if value is not None:
			return value
	return

devices_data = global_var.get_global_var("iot_devices")
devices_data = ast.literal_eval(devices_data)
id = devices_data["door magnet"]["id"]
url = REST_API + f"devices/device/{id}"
print(get_status(url))

#python -m src.external_services.iot.magnetic_contacts