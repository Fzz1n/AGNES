import threading
import sqlite3

MONTHS = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
WEEKSDAY_NAME = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
stop_event = threading.Event()
misunderstanding_counter = 0
misunderstanding_timer = None
time_left = 0

# Creation of global_var DB
def create_db():
    try:
        con = sqlite3.connect("agnes.db")
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS global_var(title TEXT UNIQUE, value)")
        data = [
            ("weather_data", None),
            ("weather_data_age", None),
            ("coordinates", None),
            ("last_answer", "No previous response"),
            ("default_energy_threshold", 200),
            ("night_light_level", 30),
            ("todays_date", None),
            ("light_data", None)
        ]
        cur.executemany("INSERT INTO global_var (title, value) VALUES (?, ?) ON CONFLICT(title) DO NOTHING", data)
        con.commit()
        print("Database Sqlite3.db formed.")
    except:
        print("Database Sqlite3.db not formed.")
    finally:
        if con:
            con.close()
            print("the sqlite connection is closed")

# Getting value from db
def get_global_var(var):
    con = sqlite3.connect("agnes.db")
    cur = con.cursor()
    raw_res = cur.execute("SELECT value FROM global_var WHERE title = ?", [var])
    res = raw_res.fetchone()
    if res is None:
        return
    return res[0]

# Chnage value in db
def set_global_var(text, var):
    con = sqlite3.connect("agnes.db")
    cur = con.cursor()
    cur.execute("UPDATE global_var SET value = ? WHERE title = ?", [var, text])
    con.commit()