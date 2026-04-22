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

# Create the body
def create_body(command):
	if "on " in command:
		return {"value":True}

	elif "off" in command:
		return {"value":False}

	elif "set" in command:
		value = converter.get_number_int(command)
		if value < 0 or value > 100:
			return "invalid percentage"
		light_level = value / 100
		return {"value": light_level}

	return

# Auto gets and store the room and light sources
def get_light_or_room(text):
	light_data = global_var.get_global_var("light_devices")
	
	# Using old data if it exist
	if light_data:
		light_data = ast.literal_eval(light_data)
	else:
		devices = get_devices()
		light_data = devices[0]

	# Find the soruce and return if it exist
	id = []
	for device_name, info in light_data.items():
		if info["room"] in text or device_name in text:
			id.append(info["id"])
	return id

def get_status(url):
	try:
		headers = {"Authorization": f"Bearer {HOMEY_KEY}"}
		r = requests.get(url, headers=headers, timeout=5)
	except:
		print("GET error. Try again later")
	else:
		# Find the value
		response = r.json()
		value = response.get("capabilitiesObj", {}).get("dim", {}).get("value")
		if value is not None:
			return value * 100
	return

# Help function for retunning an erro message
def error_msg(text):
    voice_communication.speak(text)
    return text

# Creation of the API route
def controlling_lights(command):
	global REST_API
	url = f"{REST_API}devices/device/"

	# Decidign the exicution method
	if "kill" in command or "everything off" in command:
		controlling_lights("off living room")
		controlling_lights("off bedroom")
		voice_communication.speak("copy that")
		return
	
	elif "going to bed" in command:
		controlling_lights("off living room")
		light_level = global_var.get_global_var("night_light_level")
		controlling_lights(f"set bedroom to {light_level}")
		voice_communication.speak("copy that")
		time.sleep(60 * 5) # 5 min
		controlling_lights("off bedroom")
		return

	else:
		# The input is a spesafic source or invalid 
		device_ids = get_light_or_room(command)
		if len(device_ids) == 0:
			return error_msg("Not a valid source")
		if "set" in command:
			url_end = "dim"
		else:
			url_end = "onoff"

	# Get the status from the giving sorce
	if "status" in command:
		light_level = get_status(url + device_ids[0])
		if light_level is None:
			return error_msg("No info was found")
		voice_communication.speak(f"The light level is set to: {light_level}%")
		return

	# Create and validate the body
	body = create_body(command)
	if isinstance(body, str) or body is None:
		if body is not None:
			voice_communication.speak(body)
			return
		else:
			return error_msg("Invalid execution of body")
	
	for id in device_ids:
		endpoint = url + f"{id}/capability/" + url_end
		send_req(endpoint, body)

def send_req(url, body):
	# Send request
	try:
		headers = {
			"Authorization": f"Bearer {HOMEY_KEY}",
			"Content-Type": "application/json"
		}
		r = requests.put(url, headers=headers, json=body, timeout=5)
	except:
		print("Error: make sure the correct information are inserted in the .env")
		voice_communication.speak("PUT error. Try again later")

	if r.status_code == 200:
		return
	
	return error_msg("An error acure")