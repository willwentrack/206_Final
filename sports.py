import requests
import json
import unittest
import os
import sqlite3
import shutil
import re


def fetch_field_goal_data(api_key, team, year):
    """
    Fetch field goal data for a specific team and year from the College Football Data API.

    Args:
        api_key (str): Your API key for the College Football Data API.
        team (str): Team name to fetch data for.
        year (int): Year to fetch data for.

    Returns:
        dict: Parsed JSON response from the API.
    """
    # Example API endpoint: "https://api.collegefootballdata.com/plays"
    pass

def store_field_goal_data(db_name, data):
    """
    Store field goal data in a SQLite database.

    Args:
        db_name (str): Name of the SQLite database file.
        data (dict): Field goal data to store.
    """
    # Create database schema and insert data
    pass

def calculate_paar(db_name, team):
    """
    Calculate Points Added Above Replacement (PAAR) for a team.

    Args:
        db_name (str): Name of the SQLite database file.
        team (str): Team name to calculate PAAR for.

    Returns:
        float: Calculated PAAR value.
    """
    pass