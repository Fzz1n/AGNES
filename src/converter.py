import datetime
import time
import re

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

def get_number(text):
    text = text.replace("%", "")
    array = text.split(" ")
    num = 0
    for item in array:
        res = string_to_int(item)
        if res != "":
            num = res
            break
    return num

def get_two_numbers(text):
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
            res_array.append(text_array[i + 1])
            break
    return res_array

def get_time(text):
    number = get_number(text)
    if "hours" in text:
        return number * 60 * 60
    elif "minutes" in text:
        return number * 60
    return number

def get_date(text):
    month_in_month = [month for month in src.global_var.months if month in text]

    # Year
    year = datetime.date.today().year
    if "next year" in text:
        year += 1
    
    # Month
    if not len(month_in_month):
        return "A month is missing."
    month_num = src.global_var.months[month_in_month[0]]

    # Date
    match = re.findall(r"(?<![:\d])\d+(?![:\d])", text)
    if not match:
        return "A date is missing."

    first_num = match[0]
    first_date = datetime.datetime(int(year), int(month_num), int(first_num)).date()
    
    if len(match) == 2:
        sec_num = match[1]
        # Check if the sec_num is smaller, when set the sec_num in next month 
        if int(first_num) > int(sec_num):
            # End of the year? Switch month and year
            if month_num == src.global_var.months["december"]:
                year += 1
                month_num = 1
            else:
                month_num += 1

        sec_date = datetime.datetime(int(year), int(month_num), int(sec_num)).date()

        return [first_date, sec_date]
    
    return first_date

def get_clock(text):
    match = re.findall(r"\d*:\d+", text)
    if match:
        return match
    print("No time found.")
    return