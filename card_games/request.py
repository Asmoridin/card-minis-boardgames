#!/usr/bin/python3

"""
Little module to find next set of cards in large MTG Oracle gaps
"""

import time
import os
import requests
import requests.exceptions

for x in range(7511, 8883):
    time.sleep(.75)
    URL = 'https://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=' + str(x)
    try:
        response = requests.get(URL, timeout=5)
    except requests.exceptions.ReadTimeout:
        print("Failed to read " + str(x))
        os._exit(0)
    if 'Filter by:' in response.text:
        print("Nope: " + str(x))
        continue
    print(x)
    os._exit(0)
