
import tkinter as tk
import requests
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import ttkbootstrap

def get_cesky(popis):
    match popis:
        case "overcast clouds":
            return "zataženo, mraky"
        case "light rain":
            return "jemný déšť"
        case "broken clouds":
            return "roztrhané mraky"
        case "few clouds":
            return "málo mraků"
        case "clear sky":
            return "jasno"
        case "light snow":
            return "slabé sněžení"
    return popis
def get_weather(city):
    API_key = "7ef2edbd7b0a1242681a19d0327096c6"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}"

    #print(url)

    res = requests.get(url)

    if res.status_code == 404:
        messagebox.showerror("Error", "Město nenalezeno.")
        return None

    limit = 5
    city1 = "lulec"
    url1 = f"http://api.openweathermap.org/geo/1.0/direct?q={city1}&limit={limit}&appid={API_key}"
    res1 = requests.get(url1)

    weather = res.json()
    icon_id = weather['weather'][0]['icon']
    temperature = weather['main']['temp'] - 273.15
    description = get_cesky(weather['weather'][0]['description'])
    city = weather['name']
    country = weather['sys']['country']

    icon_url = f"https://openweathermap.org/img/wn/{icon_id}@2x.png"
    return (icon_url, temperature, description, city, country)

def search():
    city = city_entry.get()
    result = get_weather(city)
    if result is None:
        return

    icon_url, temperature, description, city, country = result
    location_label.configure(text=f"{city}, {country}")

    image = Image.open(requests.get(icon_url, stream=True).raw)
    icon = ImageTk.PhotoImage(image)
    icon_label.configure(image=icon)
    icon_label.image = icon

    temperature_label.configure(text=f"Teplota: {temperature:.2f}°C")
    description_label.configure(text=f"Popis: {description}")

root = ttkbootstrap.Window(title='Předpověď počasí', themename="morph")

root.geometry("400x500")

city_entry = ttkbootstrap.Entry(root, font="Helvetica, 18")
city_entry.insert(0, "Luleč")
city_entry.pack(pady=10)

search_button = ttkbootstrap.Button(root, text="Hledat", command=search, bootstyle="warning")
search_button.pack(pady=10)

location_label = tk.Label(root, font="Helvetica, 25")
location_label.pack(pady=20)

icon_label = tk.Label(root)
icon_label.pack()

temperature_label = tk.Label(root, font="Helvetica, 20")
temperature_label.pack()

description_label = tk.Label(root, font="Helvetica, 20")
description_label.pack()

search()
root.mainloop()



