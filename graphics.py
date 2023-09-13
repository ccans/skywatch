import tkinter as tk
from storage import *
from location import *

class Graphics:

    def __init__(self):
        self.loc = Location()
        self.setup_window()
        self.setup_frames()
        self.initialize()
        self.window.mainloop()

    def setup_window(self):
        self.window = tk.Tk()
        self.window.title('skywatch')

    def setup_frames(self):
        self.input_frame = tk.Frame(master=self.window)
        self.setup_input_frame()

        self.auto_frame = tk.Frame(master=self.window)
        self.setup_auto_frame()

        self.output_frame = tk.Frame(master=self.window, padx=50)
        self.setup_output_frame()

        self.planets_frame = tk.Frame(master=self.window, pady=5)

        self.input_frame.grid(row=0, column = 0)
        self.output_frame.grid(row = 0, column = 1, rowspan=2)
        self.auto_frame.grid(row = 1, column = 0)
        self.planets_frame.grid(row = 2, column = 0, columnspan=2)

    def setup_input_frame(self):
        self.lat_label = tk.Label(master=self.input_frame, text="Enter your Latitude", padx=20, pady=10)
        self.lat_input = tk.Entry(master=self.input_frame)
        self.lat_input.insert(0, self.loc.lat)
        self.lat_label.grid(row = 0, column = 0)
        self.lat_input.grid(row = 0, column = 1)

        self.long_label = tk.Label(master=self.input_frame, text="Enter your Longitude", padx=20, pady=10)
        self.long_input = tk.Entry(master=self.input_frame)
        self.long_input.insert(0, self.loc.long)
        self.long_label.grid(row = 1, column = 0)
        self.long_input.grid(row = 1, column = 1)

    def setup_output_frame(self):
        self.output_label = tk.Label(master=self.output_frame, height=5, text="No result yet")
        self.output_label.grid(row = 0, column = 0)

        self.output_button = tk.Button(master=self.output_frame, text="Generate Output", padx=20, pady=20, command=self.generate)
        self.output_button.grid(row = 1, column = 0)

    def setup_auto_frame(self):
        self.coord_button = tk.Button(master=self.auto_frame, text="Use My Current Location (Autofill)", command=self.auto_latlng,padx=20, pady=20)
        self.coord_button.grid(row = 2, column = 0)

    def setup_planets_frame(self):
        for item in self.planets_frame.winfo_children():
            item.destroy()

        visibility_data = self.loc.planets.planets_visibility_arr
        visible_times = self.loc.weather.valid_times

        planets = ["Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]

        currentCol = 1

        for tuple in visible_times:

            lower = tuple[0]
            upper = tuple[1]

            for x in range (upper - lower + 1):
                currentTime = lower + x
                temp_label = tk.Label(master=self.planets_frame, text=self.loc.weather.convert_to_time(currentTime))
                temp_label.grid(column=currentCol, row = 0)
                currentCol = currentCol + 1
        

            for planet in range(len(planets)):
                temp_label = tk.Label(master=self.planets_frame, text=planets[planet], pady = 3)
                temp_label.grid(row = planet + 1, column = 0)

                for index in range(len(visibility_data)):
                    if visibility_data[index][planet]:
                        temp_label = tk.Label(master=self.planets_frame, text="  ", bg="blue")
                    else:
                        temp_label = tk.Label(master=self.planets_frame, text="  ", bg="red")
                    temp_label.grid(row = planet + 1, column = index + 1)

    def change_latlng(self):
        self.lat_input.delete(0, tk.END)
        self.lat_input.insert(0, self.loc.lat)

        self.long_input.delete(0, tk.END)
        self.long_input.insert(0, self.loc.long)

    def auto_latlng(self):
        self.loc.set_to_current_location()
        self.change_latlng()
        self.initialize()

    def initialize(self):
        self.output_label.config(text = self.loc.weather.weather_string)
        if self.loc.weather.valid_times != -1:
            self.setup_planets_frame()

    def generate(self):
        self.loc.set_manual_location(self.lat_input.get(), self.long_input.get())

        self.initialize()


graphics =  Graphics()