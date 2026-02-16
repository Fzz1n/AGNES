def string_to_int(s):
    try:
        num = int(s)
        return num
    except ValueError:
        #print("Invalid input: cannot convert to integer")
        return ""

def get_number(text):
    array = text.split(" ")
    num = 0
    for item in array:
        res = string_to_int(item)
        if res != "":
            num = res
            break
    return num

def get_time(text):
    number = get_number(text)
    if "hours" in text:
        return number * 60 * 60
    elif "minutes" in text:
        return number * 60
    return number