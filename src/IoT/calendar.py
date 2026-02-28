'''
THE GOAL
- upcomming next week event,
- cherrypick and check spesafic day
- create calender event, including (time/date, description, categori)
'''
import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


def authenticate_google():
	"""Shows basic usage of the Google Calendar API.
	Prints the start and name of the next 10 events on the user's calendar.
	"""
	creds = None
	# The file token.json stores the user's access and refresh tokens, and is
	# created automatically when the authorization flow completes for the first time.
	if os.path.exists("token.json"):
		creds = Credentials.from_authorized_user_file("token.json", SCOPES)
	# If there are no (valid) credentials available, let the user log in.
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

def diff_calender_id(service):
	calendar_list = service.calendarList().list().execute()
	calendars = calendar_list.get("items")
	cal_id = [cal["id"] for cal in calendars if cal["accessRole"] == "owner"]
	return cal_id

def get_events(cal_id, service, start_day, end_day = None):
	if end_day is None:
		end_day = start_day
	
	try:
		# Call the Calendar API
		start_date = datetime.datetime.combine(start_day, datetime.time.min, tzinfo=datetime.timezone.utc).isoformat()
		end_date = datetime.datetime.combine(end_day, datetime.time.max, tzinfo=datetime.timezone.utc).isoformat()

		events_res = []
		for cal_id_item in cal_id:
			result = service.events().list(
				calendarId=cal_id_item,
				timeMin=start_date,
				timeMax=end_date,
				singleEvents=True,
				orderBy="startTime"
			).execute()
			events_res.extend(result.get("items", []))

		if not events_res:
			print("No upcoming events found.")
			return
		
		# Sort the events based on when they starts
		events_res.sort(key=lambda x: x["start"].get("dateTime"))
		
		# Convert the ISO 8601 date to normal
		events_iso_free = []
		for e in events_res:
			start = datetime.datetime.fromisoformat(e["start"].get("dateTime"))
			end = datetime.datetime.fromisoformat(e["end"].get("dateTime"))
			
			event = {
				"title": e["summary"],
				"event_start": start.date(),
				"event_end": end.date(),
				"time_start": start.time(),
				"time_end": end.time()
			}

			events_iso_free.append(event)
		
		for event in events_iso_free:
			print()
			for key, info in event.items():
					print(f"{key}: {info}")
		

	except HttpError as error:
		print(f"An error occurred: {error}")

service = authenticate_google()
cal_id = diff_calender_id(service)
start = datetime.date.today()
end = datetime.date.today() + datetime.timedelta(days=6)
print("start:", start)
print("end:", end)
get_events(cal_id, service, start, end)
