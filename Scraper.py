import requests
import json

class WebScraper:
    def __init__(self, API_KEY, addresses):
        self.API_KEY = API_KEY
        self.addresses = addresses
        self.BASE_URL = 'http://dev.virtualearth.net/REST/v1/Routes'
    
    def _get_walking_distance(self, origin, destination):
        params = {
            'key': self.API_KEY,
            'wayPoint.1': origin,
            'wayPoint.2': destination,
            'routePathOutput': 'None',
            'travelMode': 'walking',
            'distanceUnit': 'km'
        }
        
        try:
            response = requests.get(self.BASE_URL, params=params)
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

    def distance(self, addresses):
        distances = {}
        locations = list(self.addresses.keys())
        
        # Initialize all location keys with empty nested dictionaries
        for location in locations:
            distances[location] = {loc: None for loc in locations}
        
        for i in range(len(locations)):
            origin = self.addresses[locations[i]]
            for j in range(i, len(locations)):
                destination = self.addresses[locations[j]]
                distance = self._get_walking_distance(origin, destination)
                if distance is not None:
                    distances[locations[i]][locations[j]] = distance
                    distances[locations[j]][locations[i]] = distance
            # Set the distance to itself as 0
            distances[locations[i]][locations[i]] = 0
        
        return distances