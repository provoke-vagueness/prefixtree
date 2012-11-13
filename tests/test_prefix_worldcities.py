import os
import sys

import csv
import shutil
import time


from prefix import Prefix
from prefix import pprint_prefix

def load(cities, src):
    with open(src,'rt',encoding='latin') as f:
        count = 0
        f.readline() #skip the header
        for row in csv.reader(f.readlines()):
            count += 1
            country, city, accentcity, region, population, lat, lon = row
            cities[city] = (lat, lon)

if __name__ == "__main__":
    s = time.time()
    try:
        cities = Prefix()
        load(cities, 'worldcitiespop.txt')
    except KeyboardInterrupt:
        pass
    print ("\nlen(cities) = %s" % len(cities))
    print("%0.2f seconds to load from csv" % (time.time() - s))

    print("Cities starting with canb:")
    for city, latlon in cities.startswith('canb'):
        print(" + %s %s" % (city, latlon))

    pprint_prefix(cities)
