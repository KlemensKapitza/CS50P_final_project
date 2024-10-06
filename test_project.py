import json
from unittest.mock import patch, mock_open, MagicMock
import pytest
from project import ISS_international_space_station, read_planets_csv, people_in_space
import sys
from prettytable import PrettyTable

def test_ISS_international_space_station():

    mock_response_data = {"iss_position": {"latitude": "-45.8951", "longitude": "-99.0023"},
                     "timestamp": 1728209528,
                     "message": "success"}
    mock_response_bytes = json.dumps(mock_response_data).encode("utf-8")

    mock_response = MagicMock()
    mock_response.read.return_value = mock_response_bytes

    with patch("urllib.request.urlopen", return_value = mock_response):
        result = ISS_international_space_station()

        assert result == "The current position of the ISS (International Space Station) is 45.8951° South 99.0023° West.\n"


def test_people_in_space():
    # number has been changed as test_data_set
    mock_response_data = {"people": [
        {"craft": "ISS", "name": "Oleg Kononenko"},
        {"craft": "ISS", "name": "Nikolai Chub"},
        {"craft": "ISS", "name": "Tracy Caldwell Dyson"},
        ], "number": 8,
         "message": "success"}

    mock_response_bytes = json.dumps(mock_response_data).encode("utf-8")
    mock_response = MagicMock()
    mock_response.read.return_value = mock_response_bytes

    with patch("urllib.request.urlopen", return_value = mock_response):
        result = people_in_space()
        assert result == "This means that 3 out of 8 people currently in space are stationed on the ISS."



def test_read_planets_csv():

    # Sample CSV for test
    MOCK_CSV_CONTENT = """planet,mass,diameter,density,gravity,escape_velocity,length_of_day,distance_from_sun,mean_temperature,number_of_moons
Earth,5.972,12742,5514,9.81,11.19,24,1.496,15,1
Mars,0.641,6779,3933,3.71,5.02,24.6,227.9,-63,2
"""
    # Use mock_open to simulate opening a file
    with patch("builtins.open", mock_open(read_data=MOCK_CSV_CONTENT)):
        #function with "Earth"
        result = read_planets_csv("Earth")

        expected_table = PrettyTable()
        expected_table.field_names = ["Attribute", "Earth Information", "Unit"]
        expected_table.add_row(["planet", "Earth", "-"])
        expected_table.add_row(["mass", "5.972", "10²⁴kg"])
        expected_table.add_row(["diameter", "12742", "km"])
        expected_table.add_row(["density", "5514", "kg/m³"])
        expected_table.add_row(["gravity", "9.81", "m/s²"])
        expected_table.add_row(["escape_velocity", "11.19", "km/s"])
        expected_table.add_row(["length_of_day", "24", "hours"])
        expected_table.add_row(["distance_from_sun", "1.496", "10⁶km"])
        expected_table.add_row(["mean_temperature", "15", "C"])
        expected_table.add_row(["number_of_moons", "1", "number"])

        assert str(result) == str(expected_table)

        # Call the function with "Mars"
        result = read_planets_csv("Mars")

        expected_table = PrettyTable()
        expected_table.field_names = ["Attribute", "Mars Information", "Unit"]
        expected_table.add_row(["planet", "Mars", "-"])
        expected_table.add_row(["mass", "0.641", "10²⁴kg"])
        expected_table.add_row(["diameter", "6779", "km"])
        expected_table.add_row(["density", "3933", "kg/m³"])
        expected_table.add_row(["gravity", "3.71", "m/s²"])
        expected_table.add_row(["escape_velocity", "5.02", "km/s"])
        expected_table.add_row(["length_of_day", "24.6", "hours"])
        expected_table.add_row(["distance_from_sun", "227.9", "10⁶km"])
        expected_table.add_row(["mean_temperature", "-63", "C"])
        expected_table.add_row(["number_of_moons", "2", "number"])

        # Assert the result is equal to expected output
        assert str(result) == str(expected_table)

        result = read_planets_csv("Venus")
        assert result is None

