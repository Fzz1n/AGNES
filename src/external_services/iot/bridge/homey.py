import os, requests, time, threading
from dotenv import load_dotenv
load_dotenv()

from src import global_var

HOMEY_KEY = os.environ["homey_key"]
HOMEY_IP_ADDRESS = os.environ["homey_ip_address"]
REST_API = f"http://{HOMEY_IP_ADDRESS}/api/manager/"

def get_rooms():
    headers = {"Authorization": f"Bearer {HOMEY_KEY}"}
    try:
        response = requests.get(REST_API + "zones/zone/", headers=headers, timeout=5)
        raw_rooms = response.json()
        rooms = {}
        for id, room in raw_rooms.items():
            rooms[id] = room['name'].lower()
        return rooms
    except:
        return "No rooms found"

def get_devices():
    rooms = get_rooms()
    if isinstance(rooms, str):
        return rooms
    
    headers = {"Authorization": f"Bearer {HOMEY_KEY}"}
    try:
        response = requests.get(REST_API + "devices/device/", headers=headers, timeout=5)
        raw_devices = response.json()
        devices = {}
        lights = {}
        for id, device in raw_devices.items():
            if device["zone"] not in rooms:
                return "Room does not exists"
            
            if "dim" in device["capabilities"]:
                lights[device["name"].lower()] = {
                    "id": id,
                    "room": rooms[device["zone"]].lower()
                }
            else:
                if device["class"] == "remote":
                    continue
                devices[f"{device['name'].lower()}_{rooms[device['zone']].lower()}"] = {
                    "id": id,
                    "room": rooms[device["zone"]].lower(),
                    "capabilities": device["capabilities"]
                }
        global_var.set_global_var("iot_devices", str(devices))
        global_var.set_global_var("light_devices", str(lights))
        return lights, devices
    except Exception as e:
        print("Fail to get IoT devices")
        return

def get_status(device_id, get_value):
    url = REST_API + f"devices/device/{device_id}"
    headers = {"Authorization": f"Bearer {HOMEY_KEY}"}
    try:
        r = requests.get(url, headers=headers, timeout=5)
        response = r.json()
        return response.get("capabilitiesObj", {}).get(get_value, {}).get("value")
    except Exception as e:
        print("GET error. Try again later", e)
        return

def auto_get_status(url, device_name, get_value, time_interval=0):
	headers = {"Authorization": f"Bearer {HOMEY_KEY}"}
	while True:
		try:
			r = requests.get(url, headers=headers, timeout=5)
			response = r.json()
			for value in get_value:
				res_value = response.get("capabilitiesObj", {}).get(value, {}).get("value")
				old_value = global_var.devices_current_values.get(device_name, {}).get(value)
				if res_value != old_value:
					if device_name not in global_var.devices_current_values:
						global_var.devices_current_values[device_name] = {}
					#print(f"[{device_name}] {value}: {res_value}")
					global_var.devices_current_values[device_name][value] = res_value
					global_var.devices_current_values[device_name]["timestamp"] = time.time()
			
		except Exception as e:
			print("GET error. Try again later", e)
		finally:
			time.sleep(time_interval)

def get_device_current_value(device_name, capability):
	return global_var.devices_current_values.get(device_name, {}).get(capability)

def update_status(device_data, devices):
    threads = []
    for device_name, config in devices.items():
        device_id = device_data[device_name]["id"]
        url = REST_API + f"devices/device/{device_id}"

        thread = threading.Thread(
            target = auto_get_status,
            args = (url, device_name, config["target_capability"], config["interval"]),
            daemon = True
        )
        thread.start()
        threads.append(thread)
    return len(threads)