#Filesystem imports for functions:
from difflib import context_diff
from floodsystem.datafetcher import fetch_measure_levels
from floodsystem.stationdata import build_station_list, update_water_levels
from floodsystem.station import inconsistent_typical_range_stations
from floodsystem.flood import risk_assessment

#Library imports:
import datetime
from itertools import groupby



def task_run(show_plot,most_severe = False):    
    stations =  build_station_list()

    # Update latest level data for all stations (to present time))
    update_water_levels(stations)
    
    consistent_stations = [station for station in stations if station.name not in inconsistent_typical_range_stations(stations)]

    dt = 3 #Number of days for levels history - too high and polyfit may not be accurate, too low and insufficient points
    p = 6 #Selecting the maximum order of the polynomial for curve fitting
    
    #Dictionary of towns followed by numerical risk scaling (discrete)
    risk_level = {}
    
    i = 0
    for station in consistent_stations:
        print('Station', i)
        i += 1
    
        dates, levels = fetch_measure_levels(station.measure_id, dt = datetime.timedelta(days = dt))
        if levels != None and len(dates) > 0:
            risk_level[station.town] = risk_assessment(station, dates, levels, p, show_plot)

    #Key note: groupby assumes the list is sorted in terms of criteria of grouping
    for key, group in groupby(sorted(risk_level,key = lambda x: risk_level[x][0]), lambda x: risk_level[x][0]):
        if most_severe == False:
            print("Risk level: {}, Towns and state of water level {}:".format(key, [(town, risk_level[town][1]) for town in group]))
        
        #If most severe == True, printing only most severe risk stations
        elif key == "SEVERE":
            print("Towns severely at risk of flooding, and state of water level: {}".format([(town, risk_level[town][1]) for town in group]))


if __name__ == "__main__":
    show_plot = False #Will show plots of water levels and linearised prediction over next 1/2 day
    task_run(show_plot, True) #True if only showing most severe towns