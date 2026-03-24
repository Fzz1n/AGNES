import os
import schedule
from src import notes
from dotenv import load_dotenv
load_dotenv()
TIMEZONE = os.environ["timezone"]

# Diff. function that shall run automatically
def jobs():
    schedule.every().monday.at("07:00", TIMEZONE).do(notes.send_note) # Sends weekley usage_report
