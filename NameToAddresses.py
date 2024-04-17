import requests



# Define the API endpoint URL
url = "https://dev.virtualearth.net/REST/v1/Autosuggest"

#Starting a for-loop for all locations

def NameToAddresses(location):
    # Create an empty list that will display all addresses found
    addresses = {}

    # Get user input for the query
    query = location

    # Define query parameters
    params = {
        "query": query,
        "includeEntityTypes": "Business,Address",
        "key": "AmSsyd6lFRUcPk43ICNzM_25im4fEI5qjjlg54c9l4Xi3lx5ys5sDVBlx98-4el0"
    }

    # Make the GET request
    response = requests.get(url, params=params)


    # Check if the request was successful
    if response.status_code == 200:
        # Parse JSON response
        data = response.json()

        # Extract name and formatted address
        for result in data['resourceSets'][0]['resources'][0]['value']:
            if 'name' in result:
                name = result['name']
                addresses[name] = "No Address"
            #   print("Name:", name)
            if 'address' in result:
                curr_address = result['address']['formattedAddress']
                addresses[name] = curr_address
                # print("Address:", name)

            else:
                name = "Unknown entity type"

        return addresses
    else:
        print("Failed to retrieve data. Status code:", response.status_code)

