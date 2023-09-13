import requests
import json
import xml.etree.ElementTree as ET
import geocoder

g = geocoder.ip('me')

timezonedb_api_key = '0L3S7KU19OC3'

# Note: Timezone API also gives the city and all that

def get_location():
    return g.latLng

def get_timezone(lat, long):
    response = requests.get('http://api.timezonedb.com/v2.1/get-time-zone?key=' + timezonedb_api_key + '&format=xml&by=position&lat=' + str(lat) + '&lng=' + str(long))
    timezone_data = ET.fromstring(response.text)
    return int(timezone_data[8].text) / 3600

def get_weather(lat, long):
    response = requests.get('https://api.open-meteo.com/v1/forecast?latitude=' + str(lat) + '&longitude=' + str(long) + '&hourly=weathercode&daily=sunrise,sunset&temperature_unit=fahrenheit&windspeed_unit=mph&precipitation_unit=inch&timezone=auto&past_days=0&forecast_days=2')
    weather_data = json.loads(response.text)
    return weather_data

def get_clearSkyTimes(weather_data):
    if "hourly" not in weather_data: 
        return -1
    weather_codes = weather_data['hourly']['weathercode']
    
    sunset_time = int(weather_data['daily']['sunset'][0].split("T")[1].split(":")[0])
    sunrise_time = int(weather_data['daily']['sunrise'][1].split("T")[1].split(":")[0])
    
    valid_times = []
    currentlyGoing = False
    blank_tuple = []
    
    for index in range(sunset_time, sunrise_time + 24):
        if weather_codes[index] <= 1: 
            if not currentlyGoing:
                currentlyGoing = True
                blank_tuple.append(index)
        else:
            if currentlyGoing:
                currentlyGoing = False
                blank_tuple.append(index)
                valid_times.append(blank_tuple)
                blank_tuple = []

    if currentlyGoing:
        blank_tuple.append(sunrise_time + 24)
        valid_times.append(blank_tuple)

    return valid_times

def get_ISOTimes(weather_data, number):
    return weather_data["hourly"]["time"][number]

# ----------------------

def convert_to_time(time):
    if time % 24 > 12:
        return str(time % 12) + " PM"
    else:
        if time % 24 == 0:
            return "12 AM"
        return str(time % 24) + " AM"

def tuple_to_timeformat(times):
    text = []
    empty_tuple = [];
    for tuple in times:
        empty_tuple.append(convert_to_time(tuple[0]))
        empty_tuple.append(convert_to_time(tuple[1]))
        text.append(empty_tuple)
        empty_tuple = []
    
    return text

def tuple_to_text(tuples):

    if tuples == -1:
        return "Invalid location"

    text_tuples = tuple_to_timeformat(tuples)

    if len(text_tuples) == 0:
        return "There are no clear times to view the night sky tonight"

    array_of_times = []

    empty_str = ""

    for text in range(len(text_tuples)):
        empty_str += text_tuples[text][0]
        empty_str += " to "
        empty_str += text_tuples[text][1]
        array_of_times.append(empty_str)
        empty_str = ""

    if(len(array_of_times) == 1):
        output_string = "Tonight, it is clear from " + array_of_times[0]
    else:
        output_string = "Tonight, it is clear from " + array_of_times[0]
        for index in range(len(array_of_times) - 2):
            output_string += ", " + array_of_times[index + 1] 
        output_string += ", and " + array_of_times[len(array_of_times) - 1]

    output_string += "."

    return output_string

planets = ["Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]

def collect_planets(lat, long):
    weather_data = get_weather(lat, long)
    visible_times = get_clearSkyTimes(weather_data)

    planets_visibility_arr = []
    
    
    for tuple in visible_times:
        lower = tuple[0]
        upper = tuple[1]

        for x in range (upper - lower + 1):
            currentTime = lower + x
            # Make the call and the creation of the planet visibility arr all in one async function
            print("https://api.visibleplanets.dev/v3?latitude=" + str(lat) + "&longitude=" + str(long) + "&time=" + get_UTC(get_ISOTimes(weather_data, currentTime), lat, long))

            resp = json.loads(requests.get("https://api.visibleplanets.dev/v3?latitude=" + str(lat) + "&longitude=" + str(long) + "&time=" + get_UTC(get_ISOTimes(weather_data, currentTime), lat, long)).text)
            
            planet_visibility_arr = [False, False, False, False, False, False, False, False]

            for point in resp["data"]:
                for planet in range(len(planets)):
                    if point["name"] == planets[planet]:
                        planet_visibility_arr[planet] = True
        
            planets_visibility_arr.append(planet_visibility_arr)
    
    return planets_visibility_arr



# Handle Timezones

from datetime import datetime
import pytz
from timezonefinder import TimezoneFinder

def get_UTC(time, lat, long):
    naive = datetime.strptime(time, "%Y-%m-%dT%H:%M")

    tf = TimezoneFinder()  
    local = pytz.timezone(tf.timezone_at(lng=float(long), lat=float(lat)))

    local_dt = local.localize(naive, is_dst=None)
    utc_dt = local_dt.astimezone(pytz.utc)

    return utc_dt.isoformat()[0:19]

# print(collect_planets(44.883, -93.283))
# print(requests.get("https://api.visibleplanets.dev/v3?latitude=32&longitude=-98").text)
