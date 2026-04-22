import os
import requests
import json
import time
from dotenv import load_dotenv
load_dotenv()
import ast

from src import calc, converter, global_var, voice_communication

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
            rooms[id] = room['name']
        return rooms
    except:
        return "No rooms found"

def get_devices():
    rooms = get_rooms()
    if isinstance(rooms, str):
        return rooms
    
    headers = {"Authorization": f"Bearer {HOMEY_KEY}"}
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
            devices[device["name"].lower()] = {
                "id": id,
                "room": rooms[device["zone"]].lower(),
                "capabilities": device["capabilities"]
            }
    global_var.set_global_var("iot_devices", str(devices))
    global_var.set_global_var("light_devices", str(lights))
    return lights, devices
