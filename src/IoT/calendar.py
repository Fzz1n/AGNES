import datetime
import re
import os.path
import src.global_var
import src.converter
import src.timer
from src.voice_communication import speak

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar"]

# Authenticate with google and auto creat a token.json
def authenticate_google():
	creds = None
	if os.path.exists("token.json"):
		creds = Credentials.from_authorized_user_file("token.json", SCOPES)

	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(
				"credentials.json", SCOPES
			)
			creds = flow.run_local_server(port=0)
		# Save the credentials for the next run
		with open("token.json", "w") as token:
			token.write(creds.to_json())
	
	service = build("calendar", "v3", credentials=creds)
	return service

# Finds the diff. calendars/groups owned by the main calendar
def owner_diff_calender(service):
	calendar_list = service.calendarList().list().execute()
	calendars = calendar_list.get("items")
	cal_info = []
	for cal in calendars:
		if cal["accessRole"] == "owner":
			if cal["id"] == cal["summary"]:
				name = "Primary"
			else:
				name = cal["summary"]
			info = {
				"name": name.lower(),
				"mail": cal["id"],
				"time_zone": cal["timeZone"]
			}
			cal_info.append(info)
	return cal_info

# Getting events basen on a target date
def get_events(cal_info, service, start_day, end_day = None):
	if end_day is None:
		end_day = start_day
	
	try:
		# Call the Calendar API
		start_date = datetime.datetime.combine(start_day, datetime.time.min, tzinfo=datetime.timezone.utc).isoformat()
		end_date = datetime.datetime.combine(end_day, datetime.time.max, tzinfo=datetime.timezone.utc).isoformat()

		events_res = []
		for cal_info_item in cal_info:
			result = service.events().list(
				calendarId=cal_info_item["mail"],
				timeMin=start_date,
				timeMax=end_date,
				singleEvents=True,
				orderBy="startTime"
			).execute()
			events_res.extend(result.get("items", []))

		if not events_res:
			return

		# Sort the events based on when they starts
		events_res.sort(key=lambda x: x["start"].get("dateTime") or x["start"].get("date"))
		
		# Convert the ISO 8601 date to normal
		events_iso_free = []
		for e in events_res:
			start_val = e["start"].get("dateTime") or e["start"].get("date")
			end_val = e["end"].get("dateTime") or e["end"].get("date")

			if start_val is None or end_val is None:
				continue 

			start = datetime.datetime.fromisoformat(start_val.replace("Z", "+00:00"))
			end = datetime.datetime.fromisoformat(end_val.replace("Z", "+00:00"))
			if "T" in start_val: # Event with time
				event = {
					"title": e.get("summary", "No title"),
					"event_start": start.date(),
					"event_end": end.date(),
					"time_start": start.time(),
					"time_end": end.time()
				}
			else:  # Full-day event
				event = {
					"title": e.get("summary", "No title"),
					"event_start": start.date(),
					"event_end": end.date(),
					"time_start": None,
					"time_end": None
				}

			events_iso_free.append(event)
		
		return events_iso_free

	except HttpError as error:
		print(f"An error occurred: {error}")
		return "An error occurred"

# Formate the return from the google calender
def calendar_output(events, specific_date):
	for event in events:
		# Starting day
		event_info = event["event_start"].strftime('%A')
		if specific_date:
			event_info = event["event_start"].strftime('%B %d')

		# Add the end date
		if event["event_start"] != event["event_end"]:
			if specific_date:
				event_info += event["event_end"].strftime('-%d')
			else:
				event_info += event["event_end"].strftime('-%A')

		# Add the title of the event
		event_info += f": {event['title']}"
		
		# Add the event's time
		if event["time_start"] is not None:
			start_t = event["time_start"].strftime('%H:%M')
			end_t = event["time_end"].strftime('%H:%M')
			event_info += f", {start_t}-{end_t}"
		
		#print(event_info)
		speak(event_info)

# 
def lookup_event(text):
	service = authenticate_google()
	cal_info = owner_diff_calender(service)
	today = datetime.date.today()
	tomorrow = today + datetime.timedelta(days=1)
	date_monday = src.timer.next_date_by_weekday(0)
	date_sunday = date_monday + datetime.timedelta(days=6)
	specific_date = False
	
	events = None
	# Depending on tehe input it getting data from eather: a week, today, tomorrow, upcoming mon- to sunday, or a inputted date
	if "week" in text:
		events = get_events(cal_info, service, date_monday, date_sunday)

	elif "today" in text:
		events = get_events(cal_info, service, today)
	
	elif "tomorrow" in text:
		events = get_events(cal_info, service, tomorrow)

	else:
		weekday_int = [src.global_var.WEEKSDAY_NAME.index(week_day) for week_day in src.global_var.WEEKSDAY_NAME if week_day in text]
		if len(weekday_int) != 0:
			# Searches for the next upcoming monday - sunday
			date = src.timer.next_date_by_weekday(weekday_int[0])
			events = get_events(cal_info, service, date)
		else:
			specific_date = True
			# An specific inserted date
			start_date = None
			end_date = None
			date = src.converter.get_date(text)
			
			# Return the res. date if a erorr accure
			if isinstance(date, str):
				return date
			elif isinstance(date, list):
				# Two date
				start_date = date[0]
				end_date = date[1]
			else:
				# One date
				start_date = date
			
			if end_date is None:
				end_date = start_date
			
			events = get_events(cal_info, service, start_date, end_date)
	
	# Return the output if any, else no data found
	if events is not None:
		calendar_output(events, specific_date)
		return
	
	return "No upcoming events"

# Creation/add of events to the Google calendar
def add_event(text):
	service = authenticate_google()
	all_cal_info = owner_diff_calender(service)
	start_date = None
	end_date = None

	# Get the date
	date = src.converter.get_date(text)
	if isinstance(date, str):
		return date
	elif isinstance(date, list):
		start_date = date[0]
		end_date = date[1]
	else:
		start_date = date
	
	if end_date is None:
		end_date = start_date

	# Title from text
	month = start_date.strftime('%B').lower()
	match = re.search(rf"calendar (.*?) {month}", text)
	if not match:
		return "Missing a title."
	title = match.group(1)

	# Target calendar
	match = re.search(r"(\w+)\s+calendar", text)
	if not match:
		return "Missing calender"
	target = match.group(1)

	calendar_id = next(
		(cal_id["mail"] for cal_id in all_cal_info if target in cal_id["name"]),
		"primary"
	)

	# Time from text
	clock = src.converter.get_clock(text)

	# If time is defined, use it
	if clock is not None:
		start_time = datetime.datetime.strptime(clock[0] + ":00", '%H:%M:%S').time()
		if len(clock) == 1:
			end_time = datetime.time.max
		else:
			end_time = datetime.datetime.strptime(clock[1] + ":00", '%H:%M:%S').time()

		start = datetime.datetime.combine(start_date, start_time).isoformat()
		end = datetime.datetime.combine(end_date, end_time).isoformat()

		event = {
			'summary': title,
			'start': {
				'dateTime': start,
				'timeZone': all_cal_info[0]["time_zone"]
			},
			'end': {
				'dateTime': end,
				'timeZone': all_cal_info[0]["time_zone"]
			}
		}

	else:
		# Full-day event
		start = start_date
		end = end_date + datetime.timedelta(days=1)
		
		event = {
			'summary': title,
			'start': {
				'date': str(start)
			},
			'end': {
				'date': str(end)
			}
		}

	try:
		event = service.events().insert(calendarId=calendar_id, body=event).execute()
	except:
		return "An error accure"
	else:
		#print('Event created: %s' % (event.get('htmlLink')))
		return "Event created"