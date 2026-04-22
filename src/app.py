import os
import time
import threading
import speech_recognition as sr
import schedule
from wakeonlan import send_magic_packet

from external_services.iot import light
from src.voice_communication import speak, get_audio
from src.external_services import weather, calendar
from src import global_var, schedules, sound_effects, calc, converter, timer, notes

def main():
    # create/update DB and save todays date in it + start schedules
    global_var.create_db()
    old_date = global_var.get_global_var("todays_date")
    schedules.jobs()

    if old_date is None:
        global_var.set_global_var("todays_date", timer.todays_date())

    # Set up microphone settings
    r = sr.Recognizer()
    r.pause_threshold = 1.0 
    r.dynamic_energy_threshold = False
    r.energy_threshold = global_var.get_global_var("default_energy_threshold")
    
    with sr.Microphone() as source:
        print("Energy threshold:", r.energy_threshold)
        
        while True:
            # r.adjust_for_ambient_noise(source, duration=1) # auto calibrate sound    
            text = get_audio(r, source, "en-US", r.energy_threshold)
            schedule.run_pending()
            if text is None or global_var.get_global_var("react_by_name") and "agnes" not in text:
                continue
            phrase = text

            if "69" in text:
                sound_effects.play_mp3("nice_meme")
            
            if "hello" in text:
                phrase = "hello"
                speak("hello, how are you?")
            elif "what's your name" in text:
                phrase = "AGNES's name"
                speak("My name is AGNES")
            elif "what does agnes stand for" in text:
                phrase = "AGNES's dif."
                speak("It stands for: Artificial Generative Nested Environment System")
            elif "who are you" in text:
                phrase = "kazoo kid"
                sound_effects.play_mp3("kazoo_kid")
            elif "hands-free mode" in text:
                phrase = "hands-free mode"
                if "deactivate" in text:
                    speak("remember to use my name when giving a command")
                    global_var.set_global_var("react_by_name", True)
                elif "activate":
                    speak("give a command without using my name")
                    global_var.set_global_var("react_by_name", False)
            elif "energy threshold" in text:
                phrase = "energy threshold"
                if "change" in text or "set" in text:
                    number = converter.get_number_int(text)
                    if not 50 <= number <= 800:
                        speak("Not a valid input")
                    else:
                        msg = f"energy threshold is now changed to: {number}"
                        if "default" in text:
                            global_var.set_global_var("default_energy_threshold", number)
                            msg = "default " + msg
                        else:
                            r.energy_threshold = number
                        speak(msg)
                elif "reading" in text:
                    speak(f"{round(r.energy_threshold, 2)}")
                elif "deactivate dynamic" in text:
                    r.dynamic_energy_threshold = False
                    r.energy_threshold = global_var.get_global_var("default_energy_threshold")
                    speak("dynamic energy threshold is now deactivated")
                elif "activate dynamic" in text:
                    r.dynamic_energy_threshold = True
                    speak("dynamic energy threshold is now activated")
            elif "deactivate microphone" in text:
                phrase = "microphone"
                speak("copy that")
                if global_var.stop_event.is_set():
                    global_var.stop_event.clear()
                sec = converter.get_time(text)
                timer.countdown(sec)
                speak("I'm back bitches!!")
            elif "time" in text:
                phrase = "timer countdown"
                if "left" in text:
                    sec = global_var.time_left
                    speak(converter.convert_seconds(sec))
                elif "stop" in text or "reset" in text:
                    global_var.stop_event.set()
                    speak("Time stopped")
                else:
                    # Reset event if set
                    if global_var.stop_event.is_set():
                        global_var.stop_event.clear()
                    
                    # Make sure a time is inserted, not e.g. 0 sec
                    sec = converter.get_time(text)
                    if sec:
                        speak("copy that")
                        t = threading.Thread(target=timer.countdown, args=(sec,))
                        t.start()
            elif "weather" in text:
                phrase = "weather"
                speak(weather.lookup_weather(text))
            elif "calculate" in text or "what is" in text:
                phrase = "calculation"
                numbers = converter.get_two_numbers_float(text)
                if numbers is None:
                    speak("Missing one or two numbers")
                else:
                    num1, num2 = numbers
                    result = None
                    
                    # Determine operation
                    if "difference" in text:
                        result = calc.ingers_equation(num1, num2)
                        is_percent = True
                    elif "+" in text or "plus" in text:
                        result = calc.addition(num1, num2)
                        is_percent = False
                    elif "-" in text or "minus" in text:
                        result = calc.subtraction(num1, num2)
                        is_percent = False
                    elif "x" in text or "times" in text:
                        result = calc.multiplication(num1, num2)
                        is_percent = False
                    elif "/" in text or "divided" in text:
                        try:
                            result = calc.division(num1, num2)
                        except ZeroDivisionError:
                            speak("Cannot divide by zero")
                            result = None
                        is_percent = False

                    # Format result
                    if result is not None:
                        if result != round(result):
                            result_str = f"approximately {round(result,1)}"
                        else:
                            result_str = str(int(result))
                        if is_percent:
                            result_str += "%"
                        speak(result_str)
            elif "rice" in text:
                phrase = "amount of rice"
                speak(f"{calc.water_to_rice(converter.get_number_and_unit(text))}")
            elif "what" in text:
                phrase = "time indication"
                if "time" in text:
                    speak(timer.current_time())
                elif "today's date" in text:
                    speak(timer.todays_date())
                elif "day is it today" in text:
                    day = timer.todays_weekday_name()
                    if day == "Wednesday":
                        sound_effects.play_mp3("it_is_wednesday")
                    else:
                        speak(day)
                elif "month" in text:
                    speak(timer.current_month_name())
                elif "week" in text:
                    speak(timer.current_week_number())
            elif "play" in text:
                phrase = "play MP3"
                if "obi-wan" in text:
                    sound_effects.play_mp3("Obi-Wan")
                elif "game" in text:
                    phrase = "start pc"
                    r.energy_threshold = 800
                    mac = os.environ["pc_mac_address"]
                    ip = os.environ["pc_ip_address"]
                    send_magic_packet(mac, ip_address=ip)
                    sound_effects.play_mp3("game_on")
            elif "adjust" in text:
                phrase = "calibrating sound output"
                if "audio" in text or "sound" in text:
                    sound_effects.adjust_sound(converter.get_number_int(text))
            elif "misunderstanding counter" in text:
                phrase = "miss. counter"
                if "reset" in text:
                    global_var.misunderstanding_counter = 0
                    speak("counter is now reset")
                else:
                    speak(f"The counter is now: {global_var.misunderstanding_counter}")
            elif "light" in text or "turn" in text or "set" in text or "going to bed" in text:
                phrase = "light"
                if "computer" in text or "pc" in text:
                    phrase = "start pc"
                    r.energy_threshold = 800
                    mac = os.environ["pc_mac_address"]
                    ip = os.environ["pc_ip_address"]
                    send_magic_packet(mac, ip_address=ip)
                elif "night" in text:
                    value = converter.get_number_int(text)
                    if value < 0 or value > 100:
                        speak("invalid percentage")
                    else:
                        global_var.set_global_var("night_light_level", value)
                        speak("changed is confirmed")
                else:
                    t = threading.Thread(target=light.controlling_lights, args=(text,))
                    t.start()
            elif "calendar" in text:
                phrase = "calendar"
                cal_res = None
                if "add" in text:
                    cal_res = calendar.add_event(text)
                else:
                    cal_res = calendar.lookup_event(text)
                
                if cal_res is not None:
                    speak(cal_res)
            elif "joke" in text:
                phrase = "telling a joke"
                speak("what do you call a cow without legs")
                time.sleep(2)
                speak("ground beef")
            elif "please repeat" in text or "come again" in text or "sorry" in text:
                phrase = "repeat of last sentence"
                speak(global_var.get_global_var("last_answer"))
            elif "send" in text:
                phrase = "reading notes"
                if "usage report" in text:
                    t = threading.Thread(target=notes.send_note)
                    t.start()
            elif "exit" in text:
                notes.write("usage_log","exit the program")
                print("Exiting program...")
                break
            
            new_date = timer.todays_date()

            # Making a new day in the usage_log, and save current date in DB
            if new_date != old_date:
                notes.write("usage_log", f"Date: {new_date}")
                global_var.set_global_var("todays_date", new_date)
                old_date = new_date

            # Add 'missing: ' in the begining of the text, for easer sorting usage_log
            if phrase is text:
                phrase = "missing: " + text
            
            # Write to the usage_log file
            notes.write("usage_log", phrase)
main()