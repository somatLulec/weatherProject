import tkinter as tk
from tkinter import  ttk
import requests
from tkinter import messagebox
from PIL import Image, ImageTk

window = tk.Tk()
window.geometry("500x400")
window.title("Předpověď počasí")

PX=5
PY=10
API_key = "7ef2edbd7b0a1242681a19d0327096c6"
c1Var = []
sel = tk.StringVar()
#data o meste a poloze
data = {}

def get_cesky_pocasi(popis):
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

def get_cesky_kraje(region):

    return region


def set_mesto(*args):
    e1.delete(0, "end")
    e1.insert(0, c1.get())

def set_box(jmesta):
    data.clear()
    i = -1
    for mesto in jmesta:
        i += 1
        combo = mesto['name'] + ', ' + get_cesky_kraje(mesto['state']) + ', ' + mesto['country']
        a = {'mesto': mesto['name'], 'lat': mesto['lat'], 'lon': mesto['lon'], 'state': mesto['state'],
             'country': mesto['country'], 'combo': combo}
        data[i] = a
        c1Var.append(combo)

def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}"

    #print(url)

    res = requests.get(url)

    if res.status_code == 404:
        c1Var.clear()

        #zkusim najit bez diakritiky
        limit = 5
        url1 = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit={limit}&appid={API_key}"
        res1 = requests.get(url1)

        if res1 == 404:
            messagebox.showerror("Error", "Město nenalezeno.")
            return None

        jmesta = res1.json()


        #naplneni mest
        set_box(jmesta)

        for i in data:
            d = dict(data[i])

            print(d['combo'])

            #print(data[i])
            #for combo in data[i]:
                #c = combo['combo']
                #print(combo)

       # https: // api.openweathermap.org / data / 2.5 / weather?lat = {lat} & lon = {lon} & appid = {APIkey}
        if len(c1Var) == 1:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={c1Var[0]}&appid={API_key}"
            res = requests.get(url)
            if res.status_code == 404:
                messagebox.showerror("Error", "Město nenalezeno.")
                return None
            e1.delete(0, "end")
            e1.insert(0, c1Var[0])
        else:
            c1.configure(values=c1Var)
            #c1.configure(data["combo"])
            c1.set(c1Var[0])
            return None

#        print(c1Var)

    weather = res.json()
    icon_id = weather['weather'][0]['icon']
    temperature = weather['main']['temp'] - 273.15
    description = get_cesky_pocasi(weather['weather'][0]['description'])
    city = weather['name']
    country = weather['sys']['country']

    icon_url = f"https://openweathermap.org/img/wn/{icon_id}@2x.png"
    return (icon_url, temperature, description, city, country)


def search_city():
    city = e1.get()
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


l1 = ttk.Label(text="Vyber obec")
l1.grid(row=0, column=0, padx = PX, pady = 3)

e1 = ttk.Entry(window)
e1.insert(0, "tucapy")
e1.grid(row=1, column = 0, padx = PX, pady = PY)

b1 = ttk.Button(window, text="Vyber", command=search_city)
b1.grid(row = 1, column = 1, padx = PX, pady = PY)

c1 = ttk.Combobox(window, values=c1Var, textvariable=sel)
c1.grid(row = 1, column = 3, padx = PX, pady = PY)

location_label = ttk.Label(window)
location_label.grid(row = 2, column = 1, padx = PX, pady = PY)

icon_label = tk.Label(window)
icon_label.grid(row = 3, column = 1, padx = PX, pady = PY)

temperature_label = tk.Label(window)
temperature_label.grid(row = 4, column = 1, padx = PX, pady = PY)

description_label = tk.Label(window)
description_label.grid(row = 5, column = 1, padx = PX, pady = PY)

sel.trace('w', set_mesto)
window.mainloop()