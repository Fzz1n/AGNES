import datetime
import time
import re
from dateutil import relativedelta

import src.global_var

def string_to_int(s):
    try:
        num = int(s)
        return num
    except ValueError:
        #print("Invalid input: cannot convert to integer")
        return ""
    
def string_to_float(s):
    try:
        num = float(s)
        return num
    except ValueError:
        #print("Invalid input: cannot convert to integer")
        return ""

def get_number_int(text):
    text = text.replace("%", "")
    array = text.split(" ")
    num = 0
    for item in array:
        res = string_to_int(item)
        if res != "":
            num = res
            break
    return num

def get_two_numbers_float(text):
    text = text.replace("%", "")
    array = text.split(" ")
    arr = []
    counter = 0
    for item in array:
        res = string_to_float(item)
        if res != "":
            counter += 1
            arr.append(res)
    if counter == 2:
        return arr
    return

def get_number_and_unit(text):
    text_array = text.split(" ")
    res_array = []
    for i, item in enumerate(text_array):
        res = string_to_float(item)
        if res != "":
            res_array.append(res)
            if i + 1 == len(text_array):
                return "a unit is missing"
            res_array.append(text_array[i + 1])
            break
    return res_array

def get_time(text):
    number = get_number_int(text)
    if "hour" in text:
        return number * 60 * 60
    elif "minute" in text:
        return number * 60
    return number

def convert_seconds(sec):
    rd = relativedelta.relativedelta(seconds=sec)
    hours = rd.hours
    minutes = rd.minutes
    seconds = rd.seconds
    if hours >= 1:
        return "{:2d}:{:2d}:{:2d}".format(hours, minutes, seconds)
    elif minutes >= 1:
        return "{:2d} min {:2d} sec".format(minutes, seconds)
    return "{:2d} sec".format(seconds)

def get_date(text):
    month_in_text = [month for month in src.global_var.MONTHS if month in text]

    # Year
    year = datetime.date.today().year
    if "next year" in text:
        year += 1
    
    # Month
    if not len(month_in_text):
        return "A month is missing."
    month_num = src.global_var.MONTHS.index(month_in_text[0]) + 1

    # Date
    match = re.findall(r"(?<![:\d])\d+(?![:\d])", text)
    if not match:
        return "A date is missing."

    first_num = match[0]
    if int(first_num) > 31 or int(first_num) < 1:
        print("invalid")
        return "The date is invalid."
    
    try:
        first_date = datetime.datetime(int(year), int(month_num), int(first_num)).date()
    except:
        return "Not a valid date."
    
    if len(match) == 2:
        sec_num = match[1]
        if int(sec_num) > 32 or int(sec_num) < 1:
            return "The date is invalid."
        # Check if the sec_num is smaller, when set the sec_num in next month 
        if int(first_num) > int(sec_num):
            # End of the year? Switch month and year
            if month_num == (src.global_var.MONTHS.index("december") + 1):
                year += 1
                month_num = 1
            else:
                month_num += 1
        try:
            sec_date = datetime.datetime(int(year), int(month_num), int(sec_num)).date()
        except:
            return "Not a valid date."
        
        return [first_date, sec_date]
    
    return first_date

def get_clock(text):
    match = re.findall(r"\d*:\d+", text)
    if match:
        return match
    print("No time found.")
    return