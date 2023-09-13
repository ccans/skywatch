from storage import *
from weather import *
from planets import *

import geocoder
import requests
import xml.etree.ElementTree as ET

class Location:

    timezonedb_api_key = '0L3S7KU19OC3'

    def __init__(self):
        self.lat = get_stored_lat()
        self.long = get_stored_long()
        self.update_timezone()
        self.handle_location_change()

    def set_to_current_location(self):
        g = geocoder.ip('me')
        self.lat = g.latlng[0]
        self.long = g.latlng[1]
        self.handle_location_change()

    def set_manual_location(self, lat, long):
        self.lat = lat
        self.long = long
        self.handle_location_change()
        
    def handle_location_change(self):
        store_data(self.lat, self.long)
        self.weather = Weather(self.lat, self.long)
        self.planets = Planets(self.weather, self.lat, self.long)

    def update_timezone(self):
        response = requests.get('http://api.timezonedb.com/v2.1/get-time-zone?key=' + self.timezonedb_api_key + '&format=xml&by=position&lat=' + str(self.lat) + '&lng=' + str(self.long))
        timezone_data = ET.fromstring(response.text)
        self.timezone = int(timezone_data[8].text) / 3600
        print(self.timezone)
    