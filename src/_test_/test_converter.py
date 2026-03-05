import src.converter

# test for getting ONE in from a string
def test_get_number_int_pass():
    text = "sting 30 test"
    assert src.converter.get_number_int(text) == 30

def test_get_number_int_pass_missing_num():
    text = "sting test"
    assert src.converter.get_number_int(text) == 0

def test_get_number_int_pass_with_double():
    text = "sting 30.21 test"
    assert src.converter.get_number_int(text) == 0

# Test for getting two floats
def test_get_two_numbers_pass():
    text = "sting 30.21 test num: two 2.1"
    assert src.converter.get_two_numbers_float(text) == [30.21, 2.1]

def test_get_two_numbers_missing_num():
    text = "sting test num: two"
    assert src.converter.get_two_numbers_float(text) is None

def test_get_two_numbers_int():
    text = "sting 30 test num: two 2"
    assert src.converter.get_two_numbers_float(text) == [30.0, 2.0]

def test_get_two_numbers_tree_num():
    text = "sting 30.4 test num: two 2.5, third: 5.2"
    assert src.converter.get_two_numbers_float(text) == [30.4, 5.2]

def test_get_two_numbers_one_num():
    text = "sting 30.4 test num"
    assert src.converter.get_two_numbers_float(text) is None


# Test for getting ONE num and ONE unit
def test_get_number_and_unit_pass():
    text = "sting 30.4 gram"
    assert src.converter.get_number_and_unit(text) == [30.4, "gram"]

def test_get_number_and_unit_missing_num():
    text = "sting gram"
    assert src.converter.get_number_and_unit(text) == []

def test_get_number_and_unit_missing_both():
    text = "sting"
    assert src.converter.get_number_and_unit(text) == []


# Test for getting a time from a string, e.g. Hour or Min.
def test_get_time_min():
    text = "30 minutes"
    res = src.converter.get_time(text)
    assert res == 30 * 60

def test_get_time_min_hour():
    text = "30 hours"
    res = src.converter.get_time(text)
    assert res == 30 * 60 * 60

def test_get_time_min_missing_num():
    text = "hours"
    res = src.converter.get_time(text)
    assert res == 0
    
def test_get_time_min_mising_format():
    text = "30"
    res = src.converter.get_time(text)
    assert res == int(text)


# Test extraction date from string
import datetime
current_year = datetime.date.today().year
month = "march"
date = "10"
def test_get_date_pass():
    text = f"{month} {date}"
    res = src.converter.get_date(text)
    assert isinstance(res, datetime.date) and str(res) == f"{current_year}-03-{date}"

def test_get_date_next_year():
    text = f"{month} {date} next year"
    res = src.converter.get_date(text)
    assert isinstance(res, datetime.date) and str(res) == f"{current_year + 1}-03-{date}"    

# Test for getting two date
def test_get_two_date_pass():
    two_date = date + " to 12"
    text = f"{month} {two_date}"
    res = src.converter.get_date(text)
    assert isinstance(res, list) and str(res[0]) == f"{current_year}-03-{date}" and str(res[1]) == f"{current_year}-03-12"

def test_get_two_date_next_year():
    two_date = date + " to 12"
    text = f"{month} {two_date} next year"
    res = src.converter.get_date(text)
    assert isinstance(res, list) and str(res[0]) == f"{current_year + 1}-03-{date}" and str(res[1]) == f"{current_year + 1}-03-12"

def test_get_two_date_end_of_month():
    two_date = date + " to 2"
    text = f"{month} {two_date}"
    res = src.converter.get_date(text)
    assert isinstance(res, list) and str(res[0]) == f"{current_year}-03-{date}" and str(res[1]) == f"{current_year}-04-02"
    
def test_get_two_date_end_of_year():
    two_date = date + " to 2"
    month = "december"
    text = f"{month} {two_date}"
    res = src.converter.get_date(text)
    assert isinstance(res, list) and str(res[0]) == f"{current_year}-12-{date}" and str(res[1]) == f"{current_year + 1}-01-02"
    
def test_get_date_missing_month():
    text = f"{date}"
    res = src.converter.get_date(text)
    assert isinstance(res, str) and res == "A month is missing."

def test_get_date_missing_date():
    text = f"{month}"
    res = src.converter.get_date(text)
    assert isinstance(res, str) and res == "A date is missing."

def test_get_date_invaild_date():
    date = "32"
    month = "february"
    text = f"{month} {date}"
    res = src.converter.get_date(text)
    assert isinstance(res, str) and res == "The date is invalid."
    
    date = "0"
    text = f"{month} {date}"
    res = src.converter.get_date(text)
    assert isinstance(res, str) and res == "The date is invalid."


# Test extraction clock from text
def test_get_clock_pass():
    time = "18:30"
    res = src.converter.get_clock(f"the time is {time} right now")
    assert res[0] == time

def test_get_clock_fail():
    res = src.converter.get_clock(f"the time is - right now")
    assert res is None