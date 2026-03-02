'''
THE GOAL
(check) - upcomming next week event,
- cherrypick and check spesafic day
- create calender event, including (time/date, description, categori)
'''
import datetime
import re
import time
import os.path
import src.global_var
import src.timer
from src.voice_communication import speak

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar"]


def authenticate_google():
	"""Shows basic usage of the Google Calendar API.
	Prints the start and name of the next 10 events on the user's calendar.
	"""
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
				"name": name,
				"mail": cal["id"],
				"time_zone": cal["timeZone"]
			}
			cal_info.append(info)
	return cal_info

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
			if "T" in start_val: # event with time
				event = {
					"title": e.get("summary", "No title"),
					"event_start": start.date(),
					"event_end": end.date(),
					"time_start": start.time(),
					"time_end": end.time()
				}
			else:  # all-day event
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
		return

def calendar_output(events):
	for event in events:
		event_info = event["event_start"].strftime('%B %d')
		if event["event_start"] != event["event_end"]:
			event_info += event["event_end"].strftime('-%d')

		event_info += f": {event['title']}"
		
		if  event["time_start"] is not None:
			start_t = event["time_start"].strftime('%H:%M')
			end_t = event["time_end"].strftime('%H:%M')
			event_info += f", {start_t}-{end_t}"
		
		print(event_info)
		#speak(event_info)

def lookup_calendar(text):
	service = authenticate_google()
	cal_info = owner_diff_calender(service)
	today = datetime.date.today()
	tomorrow = today + datetime.timedelta(days=1)
	date_monday = src.timer.next_date_by_weekday(0)
	date_sunday = date_monday + datetime.timedelta(days=6)
	
	events = None
	if "week" in text:
		events = get_events(cal_info, service, date_monday, date_sunday)

	elif "today" in text:
		events = get_events(cal_info, service, today)
	
	elif "tomorrow" in text:
		events = get_events(cal_info, service, tomorrow)

	else:
		weekday_int = [src.global_var.weeks_day_name_int[week_day] for week_day in src.global_var.weeks_day_name if week_day in text]
		if len(weekday_int) != 0:
			date = src.timer.next_date_by_weekday(weekday_int[0])
			events = get_events(cal_info, service, date)
		else:
			month_in_month = [month for month in src.global_var.months if month in text]

			if not len(month_in_month):
				return "a month is missing"
			month_num = src.global_var.months[month_in_month[0]]
			
			match = re.search(r"\d+", text)
			if not match:
				return "a date is missing"
			
			first_num = match.group()
			date = datetime.datetime(int(time.strftime("%Y")), int(month_num), int(first_num))
			events = get_events(cal_info, service, date.date())

	if events is not None:
		calendar_output(events)
		return
	
	return "No upcoming events"

def add_event(text):
	service = authenticate_google()
	all_cal_info = owner_diff_calender(service)

	'''
	# Extract info from text
	if "next year" in text:
		# cal next year

	# Month
	if not len(month_in_month):
		return "a month is missing"
	month_num = src.global_var.months[month_in_month[0]]
	
	# Date
	match = re.search(r"\d+", text)
	if not match:
		return "a date is missing"
	'''
	primary_cal = all_cal_info[0]

	event = {
		'summary': text,
		'start': {
			'dateTime': '2026-03-03T09:00:00+01:00',
			'timeZone': primary_cal["time_zone"]
		},
		'end': {
			'dateTime': '2026-03-03T17:00:00+01:00',
			'timeZone': primary_cal["time_zone"]
		}
	}

	event = service.events().insert(calendarId='primary', body=event).execute()
	print('Event created: %s' % (event.get('htmlLink')))

def test():
	''' test GET calendar data
	array = ["tuesday"] # "12th", "12th april", "april"
	for index in array:
		calender_calll = lookup_calendar(index)
		if calender_calll is not None:
			speak(calender_calll)
	'''
	'''
	service = authenticate_google()
	cal_info = owner_diff_calender(service)
	print(cal_info)
 	'''
	add_event("dette er en test2")
test()