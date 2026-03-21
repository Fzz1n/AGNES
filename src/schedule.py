import schedule
from src import notes

schedule.every().monday.at("07:00").do(notes.send_note())