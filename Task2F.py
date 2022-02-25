from cProfile import label
from turtle import color

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mplt
import datetime
import itertools

from pyparsing import col
from floodsystem.datafetcher import fetch_measure_levels

from floodsystem.flood import stations_highest_rel_level
from floodsystem.stationdata import build_station_list, update_water_levels
from floodsystem.plot import plot_water_levels






    
#Must also show the typical range Low and high for each station on the plot () 


def plot_water_level_with_fit(station, dates, levels, p, range_plot = True): #By default choose to plot the typical range High and Low

    typical_range = station.typical_range
    
    #Initially due to empty plot stations with anomalous data
    if len(levels) == 0 or len(dates) == 0: 
        print("Error: Empty Levels and Date data for Station")
    
    else:
        
    #Dates converted into float objects - required for polynomial fitting function
        x_dates = mplt.dates.date2num(dates)   
        x_dates_shift = [(date - x_dates[-1]) for date in x_dates] #Shifted by proportion of dates relative to earlier 
        #x_dates_shift: required for increased accuracy of polynomial fit

        print(station.name)
    #print(x_dates_shift)

        coeff = np.polyfit(x_dates_shift, levels, 4)  #Coefficient finding for fitting level and dates data with polynomial or degree p
    # Convert coefficient into a polynomial that can be evaluated
        poly = np.poly1d(coeff)

        plt.plot(dates, levels, color = 'r', label = "Real Data")
        plt.plot(dates, poly(x_dates_shift), color = 'b', label = "Best-fit Curve")


        if range_plot == True:
           # range_dates = np.linspace(x_dates_shift[0], x_dates_shift[-1], len(x_dates_shift))
          #  range_dates = np.linspace(dates[0], dates[-1], len(x_dates_shift))

            range_low = list(itertools.repeat(station.typical_range[0],len(x_dates_shift)))
            range_high = list(itertools.repeat(station.typical_range[1],len(x_dates_shift)))
            
            plt.plot(dates, range_low, color = 'g', label = "High line") 
            plt.plot(dates, range_high, color = '#00FA10', label = "Low line")     
            plt.xticks(rotation = 45)
            plt.legend()
       
    #Customising presentation of Graph:
        plt.legend()
        plt.xlabel("Dates: (MM DD Hr)")
        plt.ylabel("Water level")
    
        plt.xticks(rotation = 45) #Can accomodate days number easily on x-axis
        plt.title(station.name)

    #Display plot
        plt.tight_layout()  # This makes sure plot does not cut off date labels
        plt.show()

    




#External part of code: required to generate arrays of Station dictionaries, along with dates and level data

stations =  build_station_list()

    # Update latest level data for all stations
update_water_levels(stations)

M = 5 #Selecting 5 stations with hgihest water levels
level_stations = stations_highest_rel_level(stations, M)

dt = 2 #Number of days for levels history
p = 4 #Selecting the maximum order of the polynomial for curve fitting

for station in level_stations:
    dates, levels = fetch_measure_levels(station.measure_id, dt = datetime.timedelta(days = dt))
    plot_water_level_with_fit(station, dates, levels, p, True)






