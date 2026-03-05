from src.IoT.weather import lookup_weather

# Test wather
error_msg = "Couldn't find any weather projection"
def test_weather_today():
    res = lookup_weather("How is the weather today")
    assert isinstance(res, str) and res is not error_msg

def test_weather_tomorrow():
    res = lookup_weather("How is the weather tomorrow")
    assert isinstance(res, str) and res is not error_msg
    
def test_weather_week():
    res = lookup_weather("How is the weather this week")
    assert isinstance(res, str) and res is not error_msg
    
def test_weather_invalid_input():
    res = lookup_weather("not a valid weather req.")
    assert res == error_msg