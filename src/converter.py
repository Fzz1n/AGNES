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

def get_multiple_numbers(text):
    text = text.replace("%", "")
    array = text.split(" ")
    arr = []
    for item in array:
        res = string_to_float(item)
        if res != "":
            arr.append(res)
    return arr

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