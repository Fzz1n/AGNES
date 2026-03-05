import os
import time
import threading
import speech_recognition as sr

from src.voice_communication import speak, get_audio
import src.global_var
from src import sound_effects
from src import calc
from src import converter
from src import timer
from src.IoT import light, weather, calendar

def main():
    r = sr.Recognizer()
    r.dynamic_energy_threshold = False
    r.energy_threshold = 200
    r.listen
    
    with sr.Microphone() as source:
        print("Energy threshold:", r.energy_threshold)
        
        while True:    
            text = get_audio(r, source, "en-US")

            if "69" in text:
                sound_effects.play_mp3("nice_meme")
            
            if "hello" in text:
                speak("hello, how are you?")
            elif "what's your name" in text:
                speak("My name is AGNES")
            elif "what does agnes stand for" in text:
                speak("It stands for: Artificial Generative Nested Environment System")
            elif "who are you" in text:
                sound_effects.play_mp3("kazoo_kid")
            elif "energy threshold" in text:
                if "change" in text:
                    number = converter.get_number_int(text)
                    if not 50 <= number <= 800:
                        speak("Not a valid input")
                    else:
                        r.energy_threshold = number
                        speak(f"energy threshold is now changed to: {number}")
                elif "reading" in text:
                    speak(f"{round(r.energy_threshold, 2)}")
                elif "deactivate dynamic" in text:
                    r.dynamic_energy_threshold = False
                    r.energy_threshold = 200
                    speak("dynamic energy threshold is now deactivated")
                elif "activate dynamic" in text:
                    r.dynamic_energy_threshold = True
                    speak("dynamic energy threshold is now activated")
            elif "deactivate microphone" in text:
                speak("copy that")
                if src.global_var.stop_event.is_set():
                    src.global_var.stop_event.clear()
                timer.start_timer(text)
                speak("I'm back bitches!!")
            elif "timer" in text:
                if "stop" in text or "reset" in text:
                    src.global_var.stop_event.set()
                    speak("Time stopped")
                else:
                    if src.global_var.stop_event.is_set():
                        src.global_var.stop_event.clear()
                    speak("copy that")
                    t = threading.Thread(target=timer.start_timer, args=(text,))
                    t.start()
            elif "weather" in text:
                speak(weather.lookup_weather(text))
            elif "calculate" in text or "what is" in text:
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
                speak(f"{calc.water_to_rice(converter.get_number_and_unit(text))}")
            elif "what" in text:
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
                if "obi-wan" in text:
                    sound_effects.play_mp3("Obi-Wan")
                elif "game" in text:
                    sound_effects.play_mp3("game_on")
            elif "adjust" in text:
                if "audio" in text or "sound" in text:
                    sound_effects.adjust_sound(converter.get_number_int(text))
            elif "misunderstanding counter" in text:
                if "reset" in text:
                    src.global_var.misunderstanding_counter = 0
                    speak("counter is now reset")
                else:
                    speak(f"The counter is now: {src.global_var.misunderstanding_counter}")
            elif "light" in text or "turn" in text or "set" in text or "going to bed" in text:
                t = threading.Thread(target=light.controlling_lights, args=(text,))
                t.start()
            elif "calendar" in text:
                if "add" in text:
                    cal_res = calendar.add_event(text)
                    if cal_res is not None:
                        speak(cal_res)
                else:
                    calendar.lookup_event(text)
            elif "joke" in text:
                speak("what do you call a cow without legs")
                time.sleep(2)
                speak("ground beef")
            elif "please repeat" in text or "come again" in text or "sorry" in text:
                speak(src.global_var.last_answer)
            elif "exit" in text:
                print("Exiting program...")
                break
main()