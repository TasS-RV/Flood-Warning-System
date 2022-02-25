from floodsystem.datafetcher import fetch_measure_levels
from floodsystem.flood import stations_highest_rel_level
from floodsystem.stationdata import build_station_list, update_water_levels
from floodsystem.plot import plot_water_level_with_fit

import datetime



def task_run():    
#External part of code: required to generate arrays of Station dictionaries, along with dates and level data
    stations =  build_station_list()

    # Update latest level data for all stations
    update_water_levels(stations)

    M = 5 #Selecting 5 stations with hgihest water levels
    level_stations = stations_highest_rel_level(stations, M)

    dt = 2 #Number of days for levels history
    p = 4 #Selecting the maximum order of the polynomial for curve fitting
    range_plot = True #True/False to plot high and low water level lines

    for station in level_stations:
        dates, levels = fetch_measure_levels(station.measure_id, dt = datetime.timedelta(days = dt))
        plot_water_level_with_fit(station, dates, levels, p, range_plot)    


#Testing Task 2F:
if __name__ == '__main__':
    task_run()

