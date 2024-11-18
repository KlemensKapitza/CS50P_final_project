# Cosmic Insights
Author: Klemens Kapitza

This is my final project for the CS50Python course. It is my first dive into programming and my first small coding project.



Description:
Cosmic Insights is a Python Program that provides real-time data on the location of the International Space Staton (ISS), retrieves weather information
from NASA's InSight lander API and allows the user to calculate the distance between two planets in our solar system using the Skyfield library. On top of that it accesses
two csv files on planets and their satellites and provides the user with interesting information about the planet of their choice.

If the user runs the program with default settings and no additional command-line arguments, he is prompted to name a planet he wants to get more information about. Additionally
the user can chose to get information about the satellites of this planet, and if the planet of interest is Mars, the user can also chose to retrieve weather information from NASA's InSight lander API. For this functionality the program checks if the inputted planet is in the planets.csv/satellites.csv (https://www.kaggle.com/datasets/joebeachcapital/planets-and-moons?resource=download&select=planets.csv), which contains information about the planets in our solar system, plus Pluto. If the user wants to get additional information on the satellites of this planet, the program accesses the satellites.csv and outputs information about the satellites. If the user inputs a planet that is not in our solar system/in the csv files, or if the user doesn't respond with 'y' [yes] or 'n' [no] to the question whether he wants to get further information about the weather on Mars/ the satellites, the user is prompted again.
To get Mars weather data from the NASA's InSight lander API (https://science.nasa.gov/mission/insight/), the user first needs to create an API-key (https://api.nasa.gov) and set it as an environmental variable.

If the user runs the program with one additional command-line argument and this command line argument is either 'ISS', 'International Space Station' or 'Space Station',
the program accesses the open-notify 'ISS location' API (http://api.open-notify.org/iss-now.json) and receives data about the current location of the ISS in JSON format.
Additionally the program accesses the open-notify 'People in space' API (http://api.open-notify.org/astros.json) and receives data about the current number of people in space and where they are stationed. The program then returns the current location of the ISS, the crew of the ISS and the number of people that are currently in space.

Lastly, if the user runs the program and inputs the name of two planets as additional command-line arguments (so a total of three command-line arguments)
e.g.: python project.py earth mars, the program uses the Skyfield library to calculate the distance between the two planets using the ephemeris de440.bsp (in this example, the distance between Earth and Mars).

