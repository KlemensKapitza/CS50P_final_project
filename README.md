# Cosmic Insights
Author: Klemens Kapitza

Cosmic Insights: Final Project for CS50Python
Submitted: October 7, 2024  
**Cosmic Insights** is my first programming project and marks the culmination of my dive into Python programming during the CS50Python course.



Description:  

Cosmic Insights is a Python program that provides real-time data and planetary insights. It features:
- Real-time location tracking of the International Space Station (ISS) using open-notify APIs.
- Weather information retrieval for Mars via NASA's InSight lander API.
- Distance calculations between planets using the Skyfield library.
- Access to CSV data for interesting facts about planets and their natural satellites.

The program can be run interactively or with command-line arguments, offering flexible ways to explore our solar system.
If the user runs the program with default settings and no additional command-line arguments, he is prompted to name a planet he wants to get more information about. Additionally
the user can chose to get information about the satellites of this planet, and if the planet of interest is Mars, the user can also chose to retrieve weather information from NASA's InSight lander API. For this functionality the program checks if the inputted planet is in the planets.csv/satellites.csv (https://www.kaggle.com/datasets/joebeachcapital/planets-and-moons?resource=download&select=planets.csv), which contains information about the planets in our solar system, plus Pluto. If the user wants to get additional information on the satellites of this planet, the program accesses the satellites.csv and outputs information about the satellites. If the user inputs a planet that is not in our solar system/in the csv files, or if the user doesn't respond with 'y' [yes] or 'n' [no] to the question whether he wants to get further information about the weather on Mars/ the satellites, the user is prompted again.
To get Mars weather data from the NASA's InSight lander API (https://science.nasa.gov/mission/insight/), the user first needs to create an API-key (https://api.nasa.gov) and set it as an environmental variable.

If the user runs the program with one additional command-line argument and this command line argument is either 'ISS', 'International Space Station' or 'Space Station',
the program accesses the open-notify 'ISS location' API (http://api.open-notify.org/iss-now.json) and receives data about the current location of the ISS in JSON format.
Additionally the program accesses the open-notify 'People in space' API (http://api.open-notify.org/astros.json) and receives data about the current number of people in space and where they are stationed. The program then returns the current location of the ISS, the crew of the ISS and the number of people that are currently in space.

Lastly, if the user runs the program and inputs the name of two planets as additional command-line arguments (so a total of three command-line arguments)
e.g.: python project.py earth mars, the program uses the Skyfield library to calculate the distance between the two planets using the ephemeris de440.bsp (in this example, the distance between Earth and Mars).

