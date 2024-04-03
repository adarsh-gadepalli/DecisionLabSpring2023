import requests
import json

# Replace with your Bing Maps API key
API_KEY = 'AmSsyd6lFRUcPk43ICNzM_25im4fEI5qjjlg54c9l4Xi3lx5ys5sDVBlx98-4el0'

# Base URL for the Bing Maps API
BASE_URL = 'http://dev.virtualearth.net/REST/v1/Routes'

def get_walking_distance(origin, destination):
    """
    Calculates the walking distance between two locations using the Bing Maps API.

    Args:
        origin (str): The starting address.
        destination (str): The destination address.

    Returns:
        float: The walking distance in kilometers, or None if an error occurred.
    """
    params = {
        'key': API_KEY,
        'wayPoint.1': origin,
        'wayPoint.2': destination,
        'routePathOutput': 'None',
        'travelMode': 'walking',
        'distanceUnit': 'km'
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        # Extract the walking distance from the response
        if data['resourceSets']:
            resources = data['resourceSets'][0]['resources']
            if resources:
                distance = resources[0]['travelDistance']
                return distance
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

    return None

def calculate_distances(addresses):
    """
    Calculates the walking distances between all pairs of addresses in the given dictionary.

    Args:
        addresses (dict): A dictionary where keys are location names and values are addresses.

    Returns:
        dict: A dictionary where keys are location names and values are nested dictionaries
              containing the walking distances to all other locations, including itself.
    """
    distances = {}
    locations = list(addresses.keys())

    # Initialize all location keys with empty nested dictionaries
    for location in locations:
        distances[location] = {loc: None for loc in locations}

    for i in range(len(locations)):
        origin = addresses[locations[i]]
        for j in range(i, len(locations)):
            destination = addresses[locations[j]]
            distance = get_walking_distance(origin, destination)
            if distance is not None:
                distances[locations[i]][locations[j]] = distance
                distances[locations[j]][locations[i]] = distance
        # Set the distance to itself as 0
        distances[locations[i]][locations[i]] = 0

    return distances


