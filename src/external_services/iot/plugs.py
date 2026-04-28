import ast
from src import global_var
from src.external_services.iot.bridge.homey import get_status
devices_data = ast.literal_eval(global_var.get_global_var("iot_devices"))

def plugs(text):
	PLUG_DATA = devices_data["plug"]
	PLUG_DATA_ID = PLUG_DATA["id"]
    
	if "watt" in text:
		value = get_status(PLUG_DATA_ID, "measure_power")
		return value if value else 0
