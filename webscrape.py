import requests
 

def geocode_address(api_key, address):
    base_url = "http://dev.virtualearth.net/REST/v1/Locations"

    print("letian is the goat")
    
    params = {
        "query": address,
        "key": api_key,
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    try:
        coordinates = data["resourceSets"][0]["resources"][0]["point"]["coordinates"]
        return coordinates
    except (KeyError, IndexError):
        return None



def get_walking_duration(api_key, origin_address, destination_address):
    origin_coords = geocode_address(api_key, origin_address)
    destination_coords = geocode_address(api_key, destination_address)


    if origin_coords and destination_coords:
        base_url = "<http://dev.virtualearth.net/REST/v1/Routes/DistanceMatrix>"

        params = {
            "origins": f"{origin_coords[0]},{origin_coords[1]}",
            "destinations": f"{destination_coords[0]},{destination_coords[1]}",
            "travelMode": "Walking",
            "key": api_key,
        }

        response = requests.get(base_url, params=params)
        data = response.json()

        try:
            duration = data["resourceSets"][0]["resources"][0]["results"][0]["travelDuration"]
            return duration
        except (KeyError, IndexError):
            return None
    else:
        return None



def create_weights(api_key, address_dict, graph):
    weights = {}
    for location, connections in graph.items():
        weights[location] = {}
        for connection, weight in connections:
            origin_address = address_dict[location][0]
            destination_address = address_dict[connection][0]

            walking_duration = get_walking_duration(api_key, origin_address, destination_address)

            if walking_duration is not None:
                weights[location][connection] = walking_duration
            else:
                print(f"Unable to retrieve walking duration between {location} and {connection}.")

    return weights
