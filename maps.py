import geopy
import string
import pandas
import doctest-
import folium
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter


def user_input():
    """
    Takes a year from user.
    Returns a year if it is even integer, else prints caution message and
    asks for a new year.
    F.Ex. :
    -> Please enter a year: 1.4
       Oops!  That was not a valid year.  Try again...
       Please enter an even number: 1905
       1905
    """
    while True:
        try:
            year = int(input('Please enter a year:'))
            break
        except ValueError:
            print("Oops!  That was not valid year.  Try again...")
    return year


def read_file(file):
    """
    (str) -> generator
    The function reads file and returns generator of data
    """
    f = open(file, 'r', encoding='utf-8', errors='ignore')
    row = (line for line in f)
    return row


def map_1(row, year):
    """
    (generator, int) -> dict
    The function takes generator and the year and returns the dictionary with countries as keys and amount of films
    created in each country in this year.
    """
    database = dict()
    for line in row:
        yr = line.strip().split(',')[1]
        place = line.strip().split(',')[-1]
        if str(year) == yr:
            if place not in database.keys():
                database[place] = 1
            else:
                database[place] += 1
        else:
            continue
    return database


def statistics(database, year):
    """
    (dict, int) -> str
    The function takes dictionary of films and their amount and writes in txt file top_5 countries of each year.
    """
    line = "Here are top_5 locations selected by the amount of films created in " + str(year) + ":" + "\n"
    lst = [(key, value) for key, value in sorted(database.items(), key=lambda item: (item[1], item[0]))]
    for i in lst[-6:-1]:
        line += str(year) + "\n" + str(i) + "\n"
    line += 50 * "*" + "\n"
    return line

def writind_file(line1, line2, line3, line4, line5):
    f = open("Top_5.txt", "w+")
    line = line1 + line2 + line3 + line4 + line5
    f.write(line)
    f.close()


def map_2(row, year):
    """
    (generator, int) -> dict
    The function takes generator and the year and returns the dictionary with countries as keys and films names
    created in each country in this year.

    """
    database = dict()
    for line in row:
        film = line.strip().split(',')[0]
        yr = line.strip().split(',')[1]
        place = line.strip().split(',')[-1]
        if str(year) == yr:
                database[place] = film
        else:
            continue
    return database


def colors(value):
    """
    (int) -> str
    The function takes the amount of films and returns the colour for that amount.
    >>> print(colors(1))
    lightcyan
    """
    if value == 1:
        return 'lightcyan'
    elif value == 2:
        return 'aqua'
    elif value == 3:
        return 'skyblue'
    else:
        return 'cornflowerblue'


def locate(database1, database2):
    """
    (dict, dict)-> None
    The function takes twi dictionaries and builds HTML map of three slides
    """

    geolocator = Nominatim(user_agent='MAP', timeout=None)
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    map = folium.Map()
    fg = folium.FeatureGroup(name='Amount of Movies by year')
    fg_pp = folium.FeatureGroup(name="Movies by year")
    fg_ppp = folium.FeatureGroup(name="Population")

    for key, value in database1.items():
        try:
            location = geolocator.geocode(key)
            if location != None:
                coord = [location.latitude, location.longitude]
                fg.add_child(folium.CircleMarker(location=coord,
                                                 radius=10,
                                                 popup=key + '  ' + str(value),
                                                 fill_color=colors(value),
                                                 color='dodgerblue',
                                                 fill_opacity=0.7))
            else:
                continue
        except ValueError:
            continue
    for key, value in database2.items():
        try:
            location = geolocator.geocode(key)
            if location != None:
                coord = [location.latitude, location.longitude]
                fg_pp.add_child(folium.Marker(location=coord,
                                              popup=str(value),
                                              icon=folium.Icon()))
            else:
                continue
        except ValueError:
            continue

    fg_ppp.add_child(folium.GeoJson(data=open('world.json', 'r',
                                  encoding='utf-8-sig').read(),
                                  style_function=lambda x: {'fillColor': 'green'
                                  if x['properties']['POP2005'] < 10000000
                                  else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000
                                  else 'red'}))


    map.add_child(fg)
    map.add_child(fg_pp)
    map.add_child(fg_ppp)
    map.add_child(folium.LayerControl())
    map.save('Map_test.html')


if __name__ == '__main__':
    doctest.testmod()
    line1 = statistics(map_1(read_file('locations.csv'), 1905),1905)
    line2 = statistics(map_1(read_file('locations.csv'), 1906),1906)
    line3 = statistics(map_1(read_file('locations.csv'), 1907),1907)
    line4 = statistics(map_1(read_file('locations.csv'), 1908),1908)
    line5 = statistics(map_1(read_file('locations.csv'), 1909),1909)
    writind_file(line1, line2, line3, line4, line5)
    year = user_input()
    database1 = map_1(read_file('locations.csv'), year)
    database2 = map_2(read_file('locations.csv'), year)
    locate(database1, database2)

