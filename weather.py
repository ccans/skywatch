from location import * 
import requests
import json

class Weather: 

    def __init__(self, lat, long):
        self.lat = lat
        self.long = long
        self.update_weather_data()
        self.update_clear_sky_times()
        self.update_weather_string()

    def update_weather_data(self):
        response = requests.get('https://api.open-meteo.com/v1/forecast?latitude=' + str(self.lat) + '&longitude=' + str(self.long) + '&hourly=weathercode&daily=sunrise,sunset&temperature_unit=fahrenheit&windspeed_unit=mph&precipitation_unit=inch&timezone=auto&past_days=0&forecast_days=2')
        self.weather_data =  json.loads(response.text)

    def update_clear_sky_times(self):
        if "hourly" not in self.weather_data: 
            self.valid_times = -1
            return -1
        weather_codes = self.weather_data['hourly']['weathercode']
    
        sunset_time = int(self.weather_data['daily']['sunset'][0].split("T")[1].split(":")[0])
        sunrise_time = int(self.weather_data['daily']['sunrise'][1].split("T")[1].split(":")[0])
    
        valid_times = []
        blank_tuple = []

        currentlyGoing = False
        
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

        self.valid_times = valid_times

    def update_weather_string(self):
        if self.valid_times == -1:
            self.weather_string = "Invalid location"
            return -1

        text_tuples = self.tuple_to_timeformat(self.valid_times)

        if len(text_tuples) == 0:
            self.weather_string = "There are no clear times to view the night sky tonight"
            return -1

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

        self.weather_string = output_string

    def convert_to_time(self, time):
        if time % 24 > 12:
            return str(time % 12) + " PM"
        else:
            if time % 24 == 0:
                return "12 AM"
            return str(time % 24) + " AM"
        
    def tuple_to_timeformat(self, times):
        text = []
        empty_tuple = [];
        for tuple in times:
            empty_tuple.append(self.convert_to_time(tuple[0]))
            empty_tuple.append(self.convert_to_time(tuple[1]))
            text.append(empty_tuple)
            empty_tuple = []
        
        return text


