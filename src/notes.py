def write(file_name, text):
	with open(f"{file_name}.txt", "a") as f:
		f.write(text + "\n")

def creat_usage_log():
	file = "usage_log.txt"
	confirmed_msg = []
	missing_msg = []
	day_confirmed_msg = {}
	day_missing_msg = {}
	missed_count = 0
	confirmed_count = 0
	with open(file) as f:
		for line_n in f:
			line = line_n.strip()

			if line.startswith("Date: "):
				if len(day_confirmed_msg) and len(day_missing_msg):
					day_confirmed_msg["confirmed_count"] = confirmed_count
					day_missing_msg["missing_count"] = missed_count
					confirmed_msg.append(day_confirmed_msg)
					missing_msg.append(day_missing_msg)
				day_confirmed_msg = {f"{line}": 1}
				day_missing_msg = {}
				missed_count = 0
				confirmed_count = 0

			elif line.startswith("missing: "):
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

			else:
				confirmed_count += 1
				if line in day_confirmed_msg:
					day_confirmed_msg[f"{line}"] += 1
				else:
					day_confirmed_msg[f"{line}"] = 1
	day_confirmed_msg["confirmed_count"] = confirmed_count
	day_missing_msg["missing_count"] = missed_count
	confirmed_msg.append(day_confirmed_msg)
	missing_msg.append(day_missing_msg)

	# Write the usage report
	with open("usage_report.txt", "a") as f:
		for i in range(len(confirmed_msg)):
			# Date
			f.write(f"\n\n{next(iter(confirmed_msg[i]))}\n")
			
			# Confirmed messages
			f.write(f"\nConfirmed: {confirmed_msg[i]['confirmed_count']}\n")
			for key, value in list(confirmed_msg[i].items())[1:len(confirmed_msg[i])-1]:
				f.write(f"{key}: {value}\n")
			
			# Missing messages
			f.write(f"\nMissing: {missing_msg[i]['missing_count']}\n")
			for key, value in list(missing_msg[i].items())[:len(missing_msg[i])-1]:
				f.write(f"{key}: {value}\n")

creat_usage_log()