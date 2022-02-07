# Copyright (C) 2018 Garth N. Wells
#
# SPDX-License-Identifier: MIT
"""This module contains a collection of functions related to
geographical data.

"""

from .utils import sorted_by_key  # noqa
from haversine import haversine
from .station import MonitoringStation

def stations_by_distance(stations, p):
    return sorted([
        (station, haversine(station.coord, p))
    for station in stations], key=lambda x: x[1])

def stations_within_radius(stations, centre, r):
    return [station for station in stations if haversine(station.coord, centre) <= r]

def rivers_with_station(stations):
    return {station.river for station in stations}

def stations_by_river(stations):
    rivers = rivers_with_station(stations)
    station_dict = {}
    for river in rivers:
        station_dict[river] = [station for station in stations if station.river == river]

    return station_dict



#For Task 1E:

def rivers_by_station_number(stations, N):
    river_stations = [(i[0], len(i[1])) for i in stations_by_river(stations).items()]
    river_stations_sorted = sorted(river_stations, key = lambda x: x[1], reverse = True)

    top_rivers =  []
   # print(river_stations_sorted)
  
    for n, r_station in enumerate(river_stations_sorted, 1):
        if n <= N:
            top_rivers.append(r_station)

        elif n > N: #Current index is n-1
            if r_station[1] == river_stations_sorted[n-2][1]: #If number of stations matches the previous number
                top_rivers.append(r_station)
 
            else:
                break

    return top_rivers 
    
#For checking output:
#print("\n In new function:")
#print(rivers_by_station_number(stations,9))
    
    