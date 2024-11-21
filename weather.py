import requests
import json
import unittest
import os
import sqlite3
import shutil
import re
# github test

def fetch_weather_data():

    """
    Fetch weather data for a specific location and date from the Weatherstack API.
    
    Args:
        api_key (str): Your API key for Weatherstack.
        location (str): Location for which to fetch weather data.
        date (str): Date in YYYY-MM-DD format.

    Returns:
        dict: Parsed JSON response from the API.
    """
    """
    Fetch weather data for a specific location from the Visual Crossing API.
    
    Args:
        api_key (str): Your API key for Visual Crossing.
        location (str): Location for which to fetch weather data.
        unit_group (str): Unit group ('us', 'metric', etc.).
    
    Returns:
        dict: Parsed JSON response from the API.
    """

    try:
        url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/East%20Lansing/2005-08-20/2023-12-03?unitGroup=metric&key=VFBRLN44NARQS8PNBZDGBALGY&contentType=json"
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
    return None

def store_weather_data(db_name, data):
    """
    Store fetched weather data in a SQLite database.

    Args:
        db_name (str): Name of the SQLite database file.
        data (dict): Weather data to store.
    """
    # Create database schema and insert data
    pass

def calculate_precipitation(db_name, date):
    """
    Calculate total precipitation for a given date.

    Args:
        db_name (str): Name of the SQLite database file.
        date (str): Date in YYYY-MM-DD format.

    Returns:
        float: Total precipitation.
    """
    pass



