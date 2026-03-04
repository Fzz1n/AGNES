from src.IoT.calendar import add_event, lookup_event

# Tests for adding event to the calendar
create_event = "add to my calendar"
def test_add_event_with_time():
	month = "march"
	date = "4"
	title = "test python add 'normal' event"
	start_time= "18:30"
	end_time= "19:30"
	res = add_event(f"add to my calendar {title} {month} {date} at {start_time} to {end_time}")
	assert res == "Event created"
	
def test_add_full_day_event():
	month = "march"
	date = "4"
	title = "test python full day"
	res = add_event(f"add to my calendar {title} {month} {date}")
	assert res == "Event created"
    
def test_add_event_multiple_days():
	month = "march"
	date = "4 to 5"
	title = "test python multi"
	res = add_event(f"add to my calendar {title} {month} {date}")
	assert res == "Event created"
    
def test_add_event_next_year():
	month = "march"
	date = "4"
	title = "test python cal"
	start_time= "17:30"
	end_time= "18:00"
	res = add_event(f"add to my calendar {title} {month} {date} at {start_time} to {end_time} next year")
	assert res == "Event created"

def test_add_event_without_title():
	month = "march"
	date = "4"
	start_time= "17:30"
	end_time= "18:00"
	res = add_event(f"add to my calendar {month} {date} at {start_time} to {end_time} next year")
	assert res == "Missing a title."

def test_add_event_without_date():
	month = "march"
	title = "test python cal"
	start_time= "17:30"
	end_time= "18:00"
	res = add_event(f"add to my calendar {title} {month} at {start_time} to {end_time} next year")
	assert res == "A date is missing."
    
def test_add_event_without_month():
	date = "4"
	title = "test python cal"
	start_time= "17:30"
	end_time= "18:00"
	res = add_event(f"add to my calendar {title} {date} at {start_time} to {end_time}")
	assert res == "A month is missing."

def test_add_event_without_anything():
	res = add_event(f"add to my calendar")
	assert res == "A month is missing."


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
	res = lookup_event(f"{lookup_start} april 12th")
	assert res == None or res == "No upcoming events"

	res = lookup_event(f"{lookup_start} april 12")
	assert res == None or res == "No upcoming events"

	res = lookup_event(f"{lookup_start} 12 april")
	assert res == None or res == "No upcoming events"

	res = lookup_event(f"{lookup_start} 12th april")
	assert res == None or res == "No upcoming events"

def test_lookup_event_specific_date_next_year():
	res = lookup_event(f"{lookup_start} april 12th next year")
	assert res == None or res == "No upcoming events"

def test_lookup_event_missing_month():
	res = lookup_event(f"{lookup_start} 12th")
	assert res == "A month is missing."

def test_lookup_event_missing_date():
	res = lookup_event(f"{lookup_start} april")
	assert res == "A date is missing."

def test_lookup_event_missing_everyting():
	res = lookup_event(f"{lookup_start}")
	assert res == "A month is missing."