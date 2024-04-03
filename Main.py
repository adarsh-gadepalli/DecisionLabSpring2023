from Algorithm import VRP0
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
VRP0(addresses)
