import tkinter as tk
from functions_package import *

window = tk.Tk()

window.title("skywatch")

input_frame = tk.Frame(master=window)
auto_frame = tk.Frame(master=window)
output_frame = tk.Frame(master=window, padx=50)

lat_label = tk.Label(master=input_frame, text="Enter your Latitude", padx=20, pady=10)
lat_input = tk.Entry(master=input_frame)
lat_label.grid(row = 0, column = 0)
lat_input.grid(row = 0, column = 1)

long_label = tk.Label(master=input_frame, text="Enter your Longitude", padx=20, pady=10)
long_input = tk.Entry(master=input_frame)
long_label.grid(row = 1, column = 0)
long_input.grid(row = 1, column = 1)

output_label = tk.Label(master=output_frame, height=5, text="No result yet")
output_label.grid(row = 0, column = 0)

def auto_latlng():
    lat_input.delete(0, tk.END)
    lat_input.insert(0, g.latlng[0])

    long_input.delete(0, tk.END)
    long_input.insert(0, g.latlng[1])

def generate_output():
    output_label.config(text = tuple_to_text(get_clearSkyTimes(get_weather(lat_input.get(), long_input.get()))))

coord_button = tk.Button(master=auto_frame, text="Use My Current Location (Autofill)", command=auto_latlng,padx=20, pady=20)
coord_button.grid(row = 2, column = 0)

output_button = tk.Button(master=output_frame, text="Generate Output", padx=20, pady=20, command=generate_output)
output_button.grid(row = 1, column = 0)

input_frame.grid(row=0, column = 0)
output_frame.grid(row = 0, column = 1, rowspan=2)
auto_frame.grid(row = 1, column = 0)


# Run the application
window.mainloop()