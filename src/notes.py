import os
from collections import defaultdict
from src import timer, mail

def write(file_name, text):
	with open(f"{file_name}.txt", "a") as f:
		f.write(text + "\n")

def create_usage_report(year, week_no):
	firstdate, lastdate =  timer.get_date_range_from_week(year, week_no)
	file = "usage_log.txt"
	
	confirmed_msg = []
	missing_msg = []
	del_indexes = []
	current_confirmed = None
	current_missing = None

	with open(file) as f:
		for index, line_n in enumerate(f):
			line = line_n.strip()

			if line.startswith("Date: "):
				date = line.replace("Date: ", "")
				
				if date >= lastdate:
					break

				if not (firstdate <= date <= lastdate):
					continue					
				
				# Save previous day
				if current_confirmed:
					confirmed_msg.append(current_confirmed)
					missing_msg.append(current_missing)
				
				# Create new day
				current_confirmed = {
					"date": date,
					"data": defaultdict(int),
                	"count": 0
				}
				current_missing = {
					"data": defaultdict(int),
                	"count": 0
				}
				
				# Save index line for later delete
				del_indexes.append(index)

			elif current_confirmed:
				if line.startswith("missing: "):
					msg = line.replace("missing: ", "")
					current_missing["data"][msg] += 1
					current_missing["count"] += 1
				else:
					current_confirmed["data"][line] += 1
					current_confirmed["count"] += 1
				
				# Save index line for later delete
				del_indexes.append(index)
	
	if current_confirmed:
		confirmed_msg.append(current_confirmed)
		missing_msg.append(current_missing)
	else:
		return "Didn't found any logs"
	
	# Deleting the lines
	with open(file, "r") as f:
		lines = f.readlines()
	with open(file, "w") as f:
		for i, line in enumerate(lines):
			if i not in del_indexes:
				f.write(line)

	# Calc sum msg
	all_confirmed_msg = {
		"data": defaultdict(int),
        "count": 0
	}
	all_missing_msg = {
		"data": defaultdict(int),
        "count": 0
	}
	
	# Confirmed messages
	for day in confirmed_msg:
		all_confirmed_msg["count"] += day["count"]
		for key, value in day["data"].items():
			all_confirmed_msg["data"][key] += value

	# Missing messages
	for day in missing_msg:
		all_missing_msg["count"] += day["count"]
		for key, value in day["data"].items():
			all_missing_msg["data"][key] += value
	
	# Create directory
	report_path = f".usage_report/{year}/"
	create_dir(report_path)

	# Write the usage report
	with open(f"{report_path}usage_report_week-{week_no}-{year}.txt", "w") as f:
		# Total sum
		f.write(f"Total in week {week_no}\n")
		write_c_and_m(f, all_confirmed_msg, all_missing_msg)		

		# Each day
		for i in range(len(confirmed_msg)):
			# Date
			f.write(f"\n\nDate: {confirmed_msg[i]['date']}")

			# Write Confirmed and Missing in file
			write_c_and_m(f, confirmed_msg[i], missing_msg[i])

# Write Confirmed and Missing object in a file
def write_c_and_m(file, conf, miss):
	# Confirmed messages
	file.write(f"\nConfirmed: {conf['count']}\n")
	for key, value in conf["data"].items():
		file.write(f"{key}: {value}\n")
	
	# Missing messages
	file.write(f"\nMissing: {miss['count']}\n")
	for key, value in miss["data"].items():
		file.write(f"{key}: {value}\n")

# Make a new directory
def create_dir(path):
	try:
		os.mkdir(path)
		print(f"Directory '{path}' created successfully.")
	except FileExistsError:
		print(f"Directory '{path}' already exists.")
	except PermissionError:
		print(f"Permission denied: Unable to create '{path}'.")
	except Exception as e:
		print(f"An error occurred: {e}")

def send_note():
	year = timer.current_year() 
	week_now = timer.current_week_number()
	week_past = timer.current_week_number(-1)
	if week_now < week_past:
		year = str(int(year) - 1)

	res = create_usage_report(year, week_past)
	if isinstance(res, str):
		print(res)
	else:
		title = f"Week {week_past} usage report"
		file = f".usage_report/{year}/usage_report_week-{week_past}-{year}.txt"
		res = mail.send_email(title, file_path=file)
		if isinstance(res, str):
			print(res)