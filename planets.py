import json
import planets
import requests

from datetime import datetime
import pytz
from timezonefinder import TimezoneFinder

class Planets():
    
    planets = ["Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]

    def __init__(self, weather, lat, long):
        self.visible_times = weather.valid_times
        self.weather_data = weather.weather_data
        self.lat = lat
        self.long = long
        print(self.visible_times)
        if self.visible_times != -1:
            self.update_planet_visibility()


    def update_planet_visibility(self):
        planets_visibility_arr = []
        
        for tuple in self.visible_times:
            lower = tuple[0]
            upper = tuple[1]

            for x in range (upper - lower + 1):
                currentTime = lower + x

                resp = json.loads(requests.get("https://api.visibleplanets.dev/v3?latitude=" + str(self.lat) + "&longitude=" + str(self.long) + "&time=" + self.get_UTC(self.get_ISOTimes(self.weather_data, currentTime))).text)
                
                planet_visibility_arr = [False, False, False, False, False, False, False, False]

                for point in resp["data"]:
                    for planet in range(len(self.planets)):
                        if point["name"] == self.planets[planet]:
                            planet_visibility_arr[planet] = True
            
                planets_visibility_arr.append(planet_visibility_arr)
        
        self.planets_visibility_arr = planets_visibility_arr


    def get_UTC(self, time):
        naive = datetime.strptime(time, "%Y-%m-%dT%H:%M")

        tf = TimezoneFinder()  
        local = pytz.timezone(tf.timezone_at(lng=float(self.long), lat=float(self.lat)))

        local_dt = local.localize(naive, is_dst=None)
        utc_dt = local_dt.astimezone(pytz.utc)

        return utc_dt.isoformat()[0:19]
    
    def get_ISOTimes(self, weather_data, number):
        return weather_data["hourly"]["time"][number]
