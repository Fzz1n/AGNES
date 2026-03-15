import geocoder
import openmeteo_requests
import requests_cache
from retry_requests import retry
from ast import literal_eval

from src import timer
from src.global_var import WEEKSDAY_NAME, get_global_var, set_global_var

# Diff. api req: https://open-meteo.com/en/docs

def get_weather_data(lat, lon):
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": [
            "temperature_2m",               # Temperature (at 2m)
            "apparent_temperature",         # AKA feels-like temperature
            "wind_speed_10m",               # Wind speed (at 10m)
            "relative_humidity_2m",         # Humidity (at 2m)
            "precipitation",                # Total precipitation (rain, showers, snow)
            "precipitation_probability",    # The probability of the precipitation
            "snowfall",                     # Snowfall (in mm)
            "rain"                          # Rain (in mm)
        ],
        "timezone": "Europe/Berlin",
        "wind_speed_unit": "ms",
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    '''
    print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
    print(f"Elevation: {response.Elevation()} m asl")
    print(f"Timezone: {response.Timezone()}{response.TimezoneAbbreviation()}")
    print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")
    '''

    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()

    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_apparent_temperature = hourly.Variables(1).ValuesAsNumpy()
    hourly_wind_speed_10m = hourly.Variables(2).ValuesAsNumpy()
    hourly_relative_humidity_2m = hourly.Variables(3).ValuesAsNumpy()
    hourly_precipitation = hourly.Variables(4).ValuesAsNumpy()
    hourly_precipitation_probability = hourly.Variables(5).ValuesAsNumpy()
    hourly_snowfall = hourly.Variables(6).ValuesAsNumpy()
    hourly_rain = hourly.Variables(7).ValuesAsNumpy()

    weather_data = []

    for d in range(7):
        start = d * 24
        end = start + 24

        day_data = {
            "day": timer.todays_weekday_name(d).lower(),
            "min_temp": float(min(hourly_apparent_temperature[start:end])),
            "max_temp": float(max(hourly_apparent_temperature[start:end])),
            "max_wind": float(max(hourly_wind_speed_10m[start:end])),
            "max_humidity": float(max(hourly_relative_humidity_2m[start:end])),
            "max_precipitation": float(max(hourly_precipitation[start:end])),
            "total_precipitation": float(sum(hourly_precipitation[start:end])),
            "max_rain": float(max(hourly_rain[start:end])),
            "max_snow": float(max(hourly_snowfall[start:end])),
        }
        weather_data.append(day_data)

    return weather_data

# Get the posisition
def get_current_gps_coordinates():
    g = geocoder.ip('me')#this function is used to find the current information using our IP Add
    if g.latlng is not None: #g.latlng tells if the coordiates are found or not
        return g.latlng
    else:
        return None

# Collectiong the nessary weather data 
def weather_station():
    coordinates = get_global_var("coordinates")
    if coordinates is None:
        coordinates = get_current_gps_coordinates()
        if coordinates is None:
            return "Unable to retrieve your GPS coordinates."
        else:
            set_global_var("coordinates", str(coordinates))
    else:
        print(f"Using old coordinates: {coordinates}")
        coordinates = literal_eval(coordinates)
    latitude, longitude = coordinates
    
    weather_data = get_global_var("weather_data")
    if weather_data is None or timer.older_than_x_days(get_global_var("weather_data_age"), 3): # max 3 days
        print("Finding new weather data")
        weather_data = get_weather_data(latitude, longitude)
        if weather_data is None:
            return "Unable to receive weather data."
        set_global_var("weather_data", str(weather_data))
        set_global_var("weather_data_age", timer.current_time_sec())
    else:
        print("Using old wather data")
        weather_data = literal_eval(weather_data)
        
    return weather_data

# Formate the weather projection to user
def weather_forcast(item, when):
    min_t = item["min_temp"]
    max_t = item["max_temp"]
    wind = item["max_wind"]
    prec = item["total_precipitation"]
    weather_projection = f"{when} the temperature will range between {round(min_t)} and {round(max_t)} °C, with wind speeds of {round(wind)} m/s"

    if (prec > 0):
        weather_projection += f" and {round(prec)} mm of rain."
    return weather_projection

# Look up the diff. weather data giving: todat, tomorrow, or a weekday
def lookup_weather(text):
    weather_data = weather_station()
    if isinstance(weather_data, str) or weather_data is None:
        print(f"No data found, error: {weather_data}")
    
    weather_by_day = {item["day"]: item for item in weather_data}

    if "today" in text:
        today = timer.todays_weekday_name().lower()
        return weather_forcast(weather_by_day[today], "today")
    elif "tomorrow" in text:
        tomorrow = timer.todays_weekday_name(1).lower()
        return weather_forcast(weather_by_day[tomorrow], "tomorrow")
    else:
        # Weather on a inserted weekday
        for week_day in WEEKSDAY_NAME:
            if week_day in text and week_day in weather_by_day:
                return weather_forcast(weather_by_day[week_day], week_day)
                
    return "Couldn't find any weather projection"