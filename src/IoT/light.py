import os
import requests
import json
import time
from dotenv import load_dotenv
load_dotenv()

from src import calc
from src import converter

# Golden webpage to "Get started": https://developers.meethue.com/develop/get-started-2/
username = os.environ["hue_username"]
hue_ip_adress = os.environ["hue_ip_address"]
rest_api = f"http://{hue_ip_adress}/api/{username}/"

# Const for controlling the light
bri_max = 255

# Create the body
def create_body(command):
	global bri_max
	if "on " in command:
		return {"on":True}

	elif "off" in command:
		return {"on":False}

	elif "set" in command:
		value = converter.get_number(command)
		if value < 0 or value > 100:
			return "invalid percentage"
		light_level = calc.ingers_equation(bri_max, None, 100, value)
		return {"on":True, "bri":int(light_level)}

	elif "flash once" in command:
		return {"alert":"select"}

	elif "flash" in command:
		return {"alert":"lselect"}
	return

# The diffrent rooms on the HUE
def get_rooms_no(text):
	if "living" in text:
		return 81
	if "bed" in text:
		return 82
	return
	
# The diffrent connected sorces on the HUE
def deff_single_source(text):
	if "floor lamp" in text:
		return 1
	elif "dining table" in text:
		return 2
	elif "bed" in text:
		return 3
	return

def get_status(url):
	# Delete everyting from the last "/", including
	global bri_max
	url = url.rsplit("/", 1)[0]

	try:
		r = requests.get(f"{url}", timeout=5)
	except:
		print("GET error. Try again later")
	else:
		# command to extract info
		response = r.json()
		for item in response:
			if item == "state" or item == "action":
				for key, value in response["state"].items():
					if key == "bri":
						light_level = calc.ingers_equation(bri_max, value, 100)
						return round(light_level)
	return

# Creation of the API route
def controlling_lights(command):
	global rest_api
	url = None
	if "kill" in command or "everything off" in command:
		controlling_lights("off living room")
		controlling_lights("off bedroom")
		return "copy that"
	elif "going to bed" in command:
		controlling_lights("off living room")
		controlling_lights("set bedroom to 50")
		time.sleep(5 * 60) # 5 min
		controlling_lights("off bedroom")
		return "copy that"
	elif "room" in command:
		room_number = get_rooms_no(command)
		if room_number is None:
			return "the room doesn't exist"
		url = f"{rest_api}groups/{room_number}/action"
	else:
		number = deff_single_source(command)
		if number is None:
			return "Not a valid source"
		url = f"{rest_api}lights/{number}/state"

	# get the status from the giving sorce
	if "status" in command:
		light_level = get_status(url)
		if light_level is None:
			return "No info was found"
		return f"The light level is set to: {light_level}%"

	body = create_body(command)
	if isinstance(body, str) or body is None:
		if body is not None:
			return body
		else:
			return "invalid execution"

	try:
		r = requests.put(url, json.dumps(body), timeout=5)
	except:
		print("PUT error. Try again later")
	response = r.json()
	if isinstance(response, list) and "success" in response[0]:
		return ""
	return "an error acure"

print(controlling_lights("set floor lamp to 60"))
print(controlling_lights("status floor lamp"))
