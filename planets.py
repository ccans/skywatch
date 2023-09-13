import json
import planets
import requests
import aiohttp
import asyncio

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
        if self.visible_times != -1:
            asyncio.run(self.update_planet_visibility())


    async def update_planet_visibility(self):
        planets_visibility_arr = []

        async with aiohttp.ClientSession() as session:

            tasks = []
            urls = []
        
            for tuple in self.visible_times:
                lower = tuple[0]
                upper = tuple[1]

                for x in range (upper - lower + 1):
                    currentTime = lower + x
                    urls.append("https://api.visibleplanets.dev/v3?latitude=" + str(self.lat) + "&longitude=" + str(self.long) + "&time=" + self.get_UTC(self.get_ISOTimes(self.weather_data, currentTime)))
                    
            for url in urls:
                tasks.append(asyncio.ensure_future(self.get_hour_data(session, url)))
                    
            completed_tasks = await asyncio.gather(*tasks)
        
            self.planets_visibility_arr = completed_tasks

    async def get_hour_data(self, session, url):
        async with session.get(url) as resp:
            resp = await resp.json()
            planet_visibility_arr = [False, False, False, False, False, False, False, False]

            for point in resp["data"]:
                for planet in range(len(self.planets)):
                    if point["name"] == self.planets[planet]:
                        planet_visibility_arr[planet] = True
                
            return planet_visibility_arr


    def get_UTC(self, time):
        naive = datetime.strptime(time, "%Y-%m-%dT%H:%M")

        tf = TimezoneFinder()  
        local = pytz.timezone(tf.timezone_at(lng=float(self.long), lat=float(self.lat)))

        local_dt = local.localize(naive, is_dst=None)
        utc_dt = local_dt.astimezone(pytz.utc)

        return utc_dt.isoformat()[0:19]
    
    def get_ISOTimes(self, weather_data, number):
        return weather_data["hourly"]["time"][number]
