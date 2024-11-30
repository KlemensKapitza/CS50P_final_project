"""
        Cosmic Insights

        Author: Klemens Kapitza



        sources:
        for the ISS/people in space function:
            ISS location URL: http://api.open-notify.org/iss-now.json (date: 01.10.2024)
            people in space URL: http://api.open-notify.org/astros.json (date: 01.10.2024)

        for planets.csv and satellites.csv:
            https://www.kaggle.com/datasets/joebeachcapital/planets-and-moons?resource=download&select=planets.csv (date: 01.10.2024)

        for mars weather data:
            creation of an API-Key: https://api.nasa.gov (date: 01.10.2024)
            NASA's InSight lander: https://science.nasa.gov/mission/insight/ (date: 01.10.2024)

        for planetary distance calculation using the Skyfield library the ephemeris used is de440.bsp

        to install the libraries: pip install requests mars-insight prettytable skyfield
"""


import csv
import requests
import sys
import json
import os
import urllib.request
from mars_insight.api import Client
from prettytable import PrettyTable
from skyfield.api import load



def main():

        try:
            if len(sys.argv) == 1: #if there is only one command-line argument: call the informative functions
                informative_text()
                user_interaction()


            elif len(sys.argv) == 2 and sys.argv[1] in ["ISS", "International Space Station","Space Station"]: #location of the international space station (ISS)
                print(ISS_international_space_station())
                print(people_in_space())


            elif len(sys.argv) == 3: #if there are three command-line arguments: the distance between the second and third is calculated IF in ephemeris
                skyfield_operation()

            else:                    #else there was invalid input
                print("Invalid input")

        except (KeyError,ValueError):
            sys.exit("Invalid input")


def informative_text():
    print()
    print("""Here is some information before we start:

    There are 8 planets within our solar system. Pluto was once considered the ninth planet, but was reclassified as a dwarf planet by the IAU in 2006.
    I have still included Pluto in this program. For Mars, there is also additional, updated weather data available
    that has been collected by NASA's InSight Mars lander.
    The program can also give information about the satellites of the planet of interest.
    Satellites are objects that orbit a planet or a celestial body and can be divided into 2 categories: natural (moons) and artificial satellites.
    This program only provides information about natural satellites.
    The most well-known example of a natural satellite is Earth's Moon.""")
    print()


def user_interaction():
    # empty list of planets that will be filled with the planet names in the planets.csv
    planets = []

    with open("planets.csv") as file:
        #using DictReader to read the file with rows as dictionaries
        reader = csv.DictReader(file)
        # for every row in the reader the name of the planet in this row is appended to the planets list
        for row in reader:
            planets.append(row["planet"])

    # set mars_request default to None
    mars_request = None
    # ask the user which information they want to know. If there are mistakes, an Error is raised and they are promopted again.
    while True:
        try:
            user_planet = input("Which planet would you want to get more information about ? ").strip().title()
            if user_planet == "Mars":
                while True:
                    mars_request = input("There is additional updated information on Mars provided by NASA, are you interested?(y/n) ").strip().lower()
                    if mars_request in ["y","n"]:
                        break
                    elif mars_request not in ["y","n"]:
                        print("Invalid input. Please enter 'y' (yes) or 'n' (no).")

            if user_planet in planets:
                while True:
                    satellites_request = input("Would you also want to know about the satellites of this planet ?(y/n) ").strip().lower()
                    if satellites_request in ["y","n"]:
                        break
                    elif satellites_request not in ["y","n"]:
                        print("Invalid input. Please enter 'y' (yes) or 'n' (no).")
                break

            else:
                raise ValueError

        except ValueError:
            print("Please state an existing planet within our solar system.")

    # now handle the logic of the different cases (not yes is interpreted as no):
    if satellites_request == "y":
        print("\n")
        print(read_planets_csv(user_planet))
        if user_planet == "Mars" and mars_request == "y":
            print(mars_weather_data())
        print(read_satellites_csv(user_planet))

    if satellites_request != "y":
        print("\n")
        print(read_planets_csv(user_planet))
        if user_planet == "Mars" and mars_request == "y":
            print(mars_weather_data())

def read_planets_csv(user_planet):

    with open("planets.csv") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["planet"] == user_planet:

                planet_information = {}
                keys = ["planet", "mass", "diameter", "density", "gravity", "escape_velocity", "length_of_day", "distance_from_sun", "mean_temperature", "number_of_moons"]
                units =["-","10²⁴kg","km","kg/m³","m/s²","km/s","hours","10⁶km","C", "number"]
                #planet = {key: row[key] for key in keys}
                for key in keys:
                    planet_information[key] = row[key]

                table = PrettyTable()
                table.field_names = ["Attribute", f"{planet_information['planet']} Information", "Unit"]
                #table.add_row(planet_information["planet"])

                for key,unit in zip(keys,units):
                    table.add_row([key, planet_information[key], unit])
                return table

    return None


def read_satellites_csv(user_planet):

    print("\n")
    table = PrettyTable()
    table.field_names = ["Name of Satellite", "Description"]

    # open the satellites csv file
    with open("satellites.csv") as file:
        #using DictReader to read the file with rows as dictionaries
        reader = csv.DictReader(file)
        for row in reader:
            if row["planet"] == user_planet:

                name = row["name"]
                gm = row["gm"]
                radius = row["radius"]
                density = row["density"]
                magnitude = row["magnitude"]

                description = (f"This satellite has a standard gravitational parameter (GM) of {gm} km³/s², "
                               f"radius of {radius} km, \n"
                               f"a density of {density} g/cm³ and a magnitude of {magnitude}.\n")
                table.add_row([name, description])

        table.align["Name"] = "l"
        table.align["Description"] = "l"

    return table


def mars_weather_data():
    # you need to get an API key form the NASA website for the program to work: https://api.nasa.gov
    # I used an environmental variable in this script, so in order for this to work you need to copy your own API-Key into the program or set it as a env variable

    api_key = os.getenv("NASA_API_KEY")
    if not api_key:
        return ("\n NASA API key is missing. Please get a key from the NASA website https://api.nasa.gov and set it as an environmental variable or provide your key for mars weather info.")


    client = Client(api_key)
    weather = client.get_recent_weather()
    martian_day = weather.sol
    temperature = weather.temperature
    wind_speed = weather.wind_speed

    message = f"""\n
    Weather information:
    The data presented has been collected by NASA's InSight Mars lander. A martian day is commonly referred to as a sol. Today marks sol {martian_day} since the landing,
    the {temperature} with {wind_speed}.
    """
    return message


def ISS_international_space_station():
    print()
    print("The ISS moves with a speed of 28000km/h so it changes it's location really fast.")

    req = urllib.request.Request("http://api.open-notify.org/iss-now.json")
    response = urllib.request.urlopen(req)

    obj = json.loads(response.read())

    latitude, longitude =  float(obj["iss_position"]["latitude"]), float(obj["iss_position"]["longitude"])

    if latitude > 0:
        latitude = f"{latitude}° North"
    elif latitude < 0:
        latitude = f"{abs(latitude)}° South"
    else:
        latitude = "0° Equator"

    if longitude > 0:
        longitude = f"{longitude}° East"
    elif longitude < 0:
        longitude = f"{abs(longitude)}° West"
    else:
        longitude = "0° Prime Meridian"

    # message to be later returned
    return f"The current position of the ISS (International Space Station) is {latitude} {longitude}.\n"

def people_in_space():
    # Make a request to the API without the callback parameter
    req = urllib.request.Request("http://api.open-notify.org/astros.json")
    response = urllib.request.urlopen(req)

    # JSON response
    obj = json.loads(response.read())

    # number of people
    number_of_ppl = obj["number"]

    # names of people
    names = []
    people = obj["people"]
    for person in people:
        if person["craft"] == "ISS":
            names.append(person["name"])

    print(f"Right now, there are {number_of_ppl} people in space. The crew of the ISS consists of the follwing people: ")

    for name in names:
        print(name)

    return f"This means that {len(names)} out of {number_of_ppl} people currently in space are stationed on the ISS."


def skyfield_operation():

    # create timescale and ask the current time
    ts = load.timescale()
    t = ts.now()

    # Load the JPL ephemeris DE421 (covers 1900-2050)
    planets = load("de440.bsp")

    planets_mapping = {
        "jupiter": "jupiter barycenter",
        "saturn": "saturn barycenter",
        "mars": "mars barycenter",
        "earth": "earth",
        "venus": "venus",
        "mercury": "mercury",
        "uranus": "uranus barycenter",
        "neptune": "neptune barycenter",
        "pluto": "pluto barycenter",
    }

    body1_name = sys.argv[1].lower()
    body2_name = sys.argv[2].lower()

    if body1_name in planets_mapping and body2_name in planets_mapping:
        cel_object1 = planets[planets_mapping[body1_name]]
        cel_object2 = planets[planets_mapping[body2_name]]

    # The position of planet1, viewed from planet2:
        astrometric = cel_object1.at(t).observe(cel_object2)

        data = astrometric.radec()
        distance = data[2]
        print(f"""\n
        The distance between {sys.argv[1].capitalize()} and {sys.argv[2].capitalize()} is {distance}.
        1 au (astronomical unit) is a standard measurement in astronomy to describe distances within our solar system.
        It is defined as the average distance between Earth and Sun.
        1 au equals about 149.6 million kilometers.\n""")

    else:
        print(f"The celestial bodies {body1_name.capitalize()} and {body2_name.capitalize()} were not found in the ephemeris.")



if __name__ == "__main__":
    main()
