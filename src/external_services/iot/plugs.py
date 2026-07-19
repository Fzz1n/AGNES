import ast
from src import global_var
from src.external_services.iot.bridge.homey import get_status
devices_data = ast.literal_eval(global_var.get_global_var("iot_devices"))

def plugs(text):
	if "watt" in text:
		plug_name = None
		for key, value in devices_data.items():
			if "plug" in key:
				plug_name = key
			
		if plug_name is None:
			return False
		
		return get_status(devices_data[plug_name]["id"], "measure_power")
