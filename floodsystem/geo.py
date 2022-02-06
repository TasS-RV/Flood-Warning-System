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
    stations_count = []
   # river_stations = {}
    
    for n, r_station in enumerate(stations_by_river(stations).items(),0):
       # river_stations[r_station[0]] = [station.name for station in r_station[1]]  #Redundant -  Dictionary of Rivers, with list of Station names affiliated
       stations_count.append((r_station[0], len(r_station[1]))) #Tuple containing Number if Stations and River names

    stations_sorted = sorted(stations_count, key = lambda entry: entry[1], reverse= True) #2nd values stores the number of rivers 
    stations_sorted_dict = {}
    #print(stations_sorted)

    for ind, station in enumerate(stations_sorted,0):
       
        if ind > N:
            if stations_sorted[ind+1][1] == station[1]:  #If overflowing - due to 'tie' in number of stations
                stations_sorted_dict[str(station[1])].append(stations_sorted[ind+1][0]) #Adds River entry
            else:
                break #Once required number of RIvers obtained/ exceeded - stops accumulating

        elif ind <= N:
            if str(station[1]) not in stations_sorted_dict.keys():
                stations_sorted_dict[str(station[1])]  = [station[0]] #Adds River name to dicitonary of Rivers with keys as their number of Monitoring Stations
            
            else:
                stations_sorted_dict[str(station[1])].append(station[0])
    rs_output = []
    
    #Reconversion back into list of tuples: (River, Number of Stations assigned to River)
    for number, rivers in stations_sorted_dict.items():
        for r in rivers:
            rs_output.append((r, int(number)))

    return rs_output