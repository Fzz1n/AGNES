import os, schedule, threading, ast
from src import notes, global_var
from src.external_services.iot.bridge.homey import get_devices
from src.external_services.iot import magnetic_contacts, plugs, indoor_climate
from dotenv import load_dotenv
load_dotenv()
TIMEZONE = os.environ["timezone"]

# Diff. function that shall run automatically
def jobs():
    schedule.every().monday.at("07:00", TIMEZONE).do(notes.send_note) # Sends weekley usage_report
    
    # Monetoring IOT devices
    device_thread = threading.Thread(target = start_monetoring_devices, daemon = True)
    device_thread.start()

def start_monetoring_devices():
	devices_data = global_var.get_global_var("iot_devices")
	if not devices_data:
		devices_data = get_devices()
		devices_data = global_var.get_global_var("iot_devices")
	devices_data = ast.literal_eval(devices_data)

	devices_to_watch = [indoor_climate.thermometers, plugs.plugs, magnetic_contacts.manget_contacts]
	for monitor_device in devices_to_watch:
		threads = threading.Thread(
			target = monitor_device,
			args = (devices_data.copy(),),
			daemon = True
		)
		threads.start()