from src.IoT.calendar import add_event, lookup_event

def test_add_event():
	month = "march"
	date = "4"
	title = "test python cal"
	start_time= "18:30"
	end_time= "19:30"
	ad = add_event(f"add to my calendar {title} {month} {date} at {start_time} to {end_time}")
	print(ad)
	ad = add_event(f"add to my calendar {title} {month} {date} at {start_time}")
	ad = add_event(f"add to my calendar {title} {month} {date}")
	ad = add_event(f"add to my calendar {month} {date}")
	ad = add_event(f"add to my calendar {title} {date}")
	ad = add_event(f"add to my calendar {title} {month} at {start_time}")
	ad = add_event(f"add to my calendar {title} {month} {date} at {start_time} to {end_time}")
	print(ad)
	date = "4 to 5"
	ad = add_event(f"add to my calendar {title} {month} {date} at {start_time} to {end_time}")
	print(ad)
	date = "20 to 4"
	ad = add_event(f"add to my calendar {title} {month} {date} at {start_time} to {end_time}")
	# test GET calendar data
	array = ["wednesday", "12th", "12th april", "april 12th", "april", "april 12"]
	for index in array:
		calender_calll = lookup_event(index)
		if calender_calll is not None:
			print(calender_calll)

	# test for adding event across multibel days

# Test lookup in the calendar
lookup_start = "anything in my calendar"
def test_lookup_event_week():
	res = lookup_event(f"{lookup_start} next week")
	assert res == None or res == "No upcoming events"

def test_lookup_event_today():
	res = lookup_event(f"{lookup_start} today")
	assert res == None or res == "No upcoming events"

def test_lookup_event_tomorrow():
	res = lookup_event(f"{lookup_start} tomorrow")
	assert res == None or res == "No upcoming events"
	
def test_lookup_event_random_week_day():
	res = lookup_event(f"{lookup_start} on friday")
	assert res == None or res == "No upcoming events"

def test_lookup_event_specific_date():
	res = lookup_event(f"{lookup_start} April 12th")
	assert res == None or res == "No upcoming events"

	res = lookup_event(f"{lookup_start} April 12")
	assert res == None or res == "No upcoming events"

	res = lookup_event(f"{lookup_start} 12 April")
	assert res == None or res == "No upcoming events"

	res = lookup_event(f"{lookup_start} 12th April")
	assert res == None or res == "No upcoming events"

def test_lookup_event_specific_date_next_year():
	res = lookup_event(f"{lookup_start} April 12th next year")
	assert res == None or res == "No upcoming events"

def test_lookup_event_missing_month():
	res = lookup_event(f"{lookup_start} 12th")
	assert res == "A month is missing."

def test_lookup_event_missing_date():
	res = lookup_event(f"{lookup_start} April")
	assert res == "A date is missing."

def test_lookup_event_missing_everyting():
	res = lookup_event(f"{lookup_start}")
	assert res == "A month is missing."