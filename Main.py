from Algorithm import VehicleRoutingProblemAlgorithm as VRP
from Scraper import WebScraper

# Replace with your Bing Maps API key
API_KEY = 'AmSsyd6lFRUcPk43ICNzM_25im4fEI5qjjlg54c9l4Xi3lx5ys5sDVBlx98-4el0'

#Dictionary of addresses of POIs
#Maybe create another Scraper-eque class file that scrapes for addresses and creates a dictionary of them
#using data from front-end?
addresses = {
    'Burj': '1 Mohammed Bin Rashid Boulevard, Downtown Dubai, Dubai 9440',
    'Mall': 'Sheikh Mohammed bin Rashid Boulevard Address Dubai Mall, Dubai',
    'Opera': '25898 87691, Dubai, Dubai',
    'Ski': 'Mall of the Emirates, Dubai',
    'Garden': 'Al Barsha South 3, Dubai United Arab Emirates 00000'
}

#Using Scraper class here to scrape with our API key and the given dictionary of addresses.
scraper = WebScraper(API_KEY, addresses)
distance_matrix = scraper.distance(addresses)

#Small piece of code that converts scraper output into a form that is used by Algorithm
#Honestly, could just make this a part of the Scraper and make Main.py look cleaner.
#This is a later Shammas task.
big_matrix = []
for loc, nbrs in distance_matrix.items():
    local_matrix = []
    for nbr, dist in nbrs.items():
        local_matrix.append(int(dist))
    big_matrix.append(local_matrix)

#Data initialization for Algorithm.
#Will be connecting front end to this part of backend as well
num_days = 1
hotel_index = 0
all_locations = list(addresses.keys())

#Solving using Vehicle Routing Problem Solution
vrp = VRP(big_matrix, num_days, hotel_index)
vrp.solve(all_locations)