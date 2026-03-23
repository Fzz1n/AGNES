import os
import requests
import json
import time
from dotenv import load_dotenv
load_dotenv()
import ast
from collections import defaultdict

from src import calc, converter, global_var, voice_communication

# Golden webpage to "Get started": https://developers.meethue.com/develop/get-started-2/
USERNAME = os.environ["hue_username"]
HUE_IP_ADDRESS = os.environ["hue_ip_address"]
REST_API = f"http://{HUE_IP_ADDRESS}/api/{USERNAME}/"

# Const for controlling the light
BRI_MAX = 255

# Create the body
def create_body(command):
	global BRI_MAX
	if "on " in command:
		return {"on":True}

	elif "off" in command:
		return {"on":False}

	elif "set" in command:
		value = converter.get_number_int(command)
		if value < 0 or value > 100:
			return "invalid percentage"
		light_level = calc.ingers_equation(BRI_MAX, None, 100, value)
		return {"on":True, "bri":int(light_level)}

	elif "flash once" in command:
		return {"alert":"select"}

	elif "flash" in command:
		return {"alert":"lselect"}
	return

# Auto gets and store the room and light sources
def get_light_or_room(text):
	light_data = global_var.get_global_var("light_data")
	
	# Using old data if it exist
	if light_data:
		print("Using old light data")
		light_data = ast.literal_eval(light_data)
	else:
		# Getting new data soruces
		r = requests.get(f"{REST_API}", timeout=5)
		response = r.json()
		light_data = {
			"rooms": {},
			"lights": {}
		}

		# Finding rooms
		for room_no, data in response["groups"].items():
			if data["type"] == "Room":
				light_data["rooms"][data["name"].lower()] = room_no
	
		# Finding lights
		for light_no, data in response["lights"].items():
			if data["type"] == "Dimmable light":
				light_data["lights"][data["name"].lower()] = light_no

		if light_data is None:
			return
		# Save in DB
		global_var.set_global_var("light_data", str(light_data))

	# Find the soruce and return if it exist
	number = [n for location, data in light_data.items() for source, n in data.items() if source in text]
	if number:
		return int(number[0])
	return

def get_status(url):
	# Delete everyting from the last "/", including
	global BRI_MAX
	url = url.rsplit("/", 1)[0]

	try:
		r = requests.get(f"{url}", timeout=5)
	except:
		print("GET error. Try again later")
	else:
		# Command to extract info
		response = r.json()
		for item in response:
			if item == "state" or item == "action":
				for key, value in response["state"].items():
					if key == "bri":
						light_level = calc.ingers_equation(BRI_MAX, value, 100)
						return round(light_level)
	return

# Help function for retunning an erro message
def error_msg(text):
    voice_communication.speak(text)
    return text

# Creation of the API route
def controlling_lights(command):
	global REST_API
	url = None

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
		time.sleep(5 * 60) # 5 min
		controlling_lights("off bedroom")
		return

	elif "room" in command:
		room_number = get_light_or_room(command)
		if room_number is None:
			return error_msg("the room doesn't exist")
		url = f"{REST_API}groups/{room_number}/action"

	else:
		# The input is a spesafic source or invalid 
		number = get_light_or_room(command)
		if number is None:
			return error_msg("Not a valid source")
		url = f"{REST_API}lights/{number}/state"

	# Get the status from the giving sorce
	if "status" in command:
		light_level = get_status(url)
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

	# Send request
	try:
		r = requests.put(url, json.dumps(body), timeout=5)
	except:
		print("Error: make sure the correct information are inserted in the .env")
		voice_communication.speak("PUT error. Try again later")

	response = r.json()
	if isinstance(response, list) and "success" in response[0]:
		return
	
	return error_msg("An error acure")