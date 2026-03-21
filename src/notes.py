import os
from src import timer
from src import mail

def write(file_name, text):
	with open(f"{file_name}.txt", "a") as f:
		f.write(text + "\n")

def create_usage_report(year, week_no):
	firstdate, lastdate =  timer.get_date_range_from_week(year, week_no)
	file = "usage_log.txt"
	confirmed_msg = []
	missing_msg = []
	day_confirmed_msg = {}
	day_missing_msg = {}
	missed_count = 0
	confirmed_count = 0
	found_first_date = False
	del_indexes = []
	with open(file) as f:
		for index, line_n in enumerate(f):
			line = line_n.strip()

			if line.startswith("Date: "):
				date = line.replace("Date: ", "")
				
				if date >= lastdate:
					break

				if date >= firstdate and date <= lastdate:
					found_first_date = True
				else:
					continue

				if len(day_confirmed_msg) and len(day_missing_msg):
					day_confirmed_msg["confirmed_count"] = confirmed_count
					day_missing_msg["missing_count"] = missed_count
					confirmed_msg.append(day_confirmed_msg)
					missing_msg.append(day_missing_msg)
				day_confirmed_msg = {f"date": date}
				day_missing_msg = {}
				missed_count = 0
				confirmed_count = 0
				
				del_indexes.append(index)

			elif line.startswith("missing: ") and found_first_date:
				# Remove missing from the begining of the string
				missed_info = line.replace("missing: ", "")
				missed_count += 1
				
				if len(day_missing_msg) == 0:
					day_missing_msg[f"{missed_info}"] = 1

				else:
					if missed_info in day_missing_msg:
						day_missing_msg[f"{missed_info}"] += 1
					else:
						day_missing_msg[f"{missed_info}"] = 1
				
				del_indexes.append(index)

			elif found_first_date:
				confirmed_count += 1
				if line in day_confirmed_msg:
					day_confirmed_msg[f"{line}"] += 1
				else:
					day_confirmed_msg[f"{line}"] = 1
				
				del_indexes.append(index)
	
	day_confirmed_msg["confirmed_count"] = confirmed_count
	day_missing_msg["missing_count"] = missed_count
	confirmed_msg.append(day_confirmed_msg)
	missing_msg.append(day_missing_msg)

	if not found_first_date:
		return "Didn't found any logs"
	
	# Deleting the lines
	with open(file, "r") as f:
		lines = f.readlines()
	with open(file, "w") as f:
		for i, line in enumerate(lines):
			if i not in del_indexes:
				f.write(line)

	report_path = f".usage_report/{year}/"
	create_dir(report_path)

	# Write the usage report
	found_first_date = False
	with open(f"{report_path}usage_report_week-{week_no}-{year}.txt", "w") as f:
		all_confirmed_msg = {}
		all_missing_msg = {}
		# Calc sum msg
		for i in range(len(confirmed_msg)):
			# Confirmed messages
			for key, value in list(confirmed_msg[i].items())[1:]:
				if key in all_confirmed_msg:
					all_confirmed_msg[f"{key}"] += value
				else:
					all_confirmed_msg[f"{key}"] = value
			
			# Missing messages
			for key, value in missing_msg[i].items():
				if key in all_missing_msg:
					all_missing_msg[f"{key}"] += value
				else:
					all_missing_msg[f"{key}"] = value

		# Total sum
		f.write(f"Total in week {week_no}\n")
		f.write(f"\nConfirmed: {all_confirmed_msg['confirmed_count']}\n")
		del all_confirmed_msg['confirmed_count']
		for key, value in all_confirmed_msg.items():
			f.write(f"{key}: {value}\n")
		f.write(f"\nMissing: {all_missing_msg['missing_count']}\n")
		del all_missing_msg['missing_count']
		for key, value in all_missing_msg.items():
			f.write(f"{key}: {value}\n")
		

		for i in range(len(confirmed_msg)):			
			# Date
			f.write(f"\n\nDate: {confirmed_msg[i]['date']}")
			
			# Confirmed messages
			f.write(f"\nConfirmed: {confirmed_msg[i]['confirmed_count']}\n")
			for key, value in list(confirmed_msg[i].items())[1:len(confirmed_msg[i])-1]:
				f.write(f"{key}: {value}\n")
			
			# Missing messages
			f.write(f"\nMissing: {missing_msg[i]['missing_count']}\n")
			for key, value in list(missing_msg[i].items())[:len(missing_msg[i])-1]:
				f.write(f"{key}: {value}\n")

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
		else:
			print