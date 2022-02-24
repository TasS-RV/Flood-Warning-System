from cProfile import label
from turtle import color

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mplt
import datetime
import math

from pyparsing import col
from floodsystem.datafetcher import fetch_measure_levels

from floodsystem.flood import stations_highest_rel_level
from floodsystem.stationdata import build_station_list, update_water_levels
from floodsystem.plot import plot_water_levels






    
#Must also show the typical range Low and high for each station on the plot () 


def plot_water_level_with_fit(station, dates, levels, p):

    typical_range = station.typical_range

    if len(levels) == 0 or len(dates) == 0:
        print("Error: Empty Levels and Date data for Station")
    
    else:
        
    #Dates converted into float objects - required for polynomial fitting function
        x_dates = mplt.dates.date2num(dates)   
        x_dates_shift = [(date - x_dates[-1]) for date in x_dates] #Shifted by proportion of dates relative to earlier (-10 days from now) 

        print(station.name)
    #print(x_dates_shift)

        coeff = np.polyfit(x_dates_shift, levels, 4)  #Coefficient finding for fitting level and dates data with polynomial or degree p
    # Convert coefficient into a polynomial that can be evaluated
        poly = np.poly1d(coeff)

    
        plt.plot(x_dates_shift, levels, color = 'r', label = "Real Data")
        plt.plot(x_dates_shift, poly(x_dates_shift), color = 'b', label = "Best-fit Curve")
         

        middle_date = x_dates_shift[math.floor(len(x_dates_shift)/2)]

        plt.scatter([middle_date, middle_date], typical_range, color = 'g', s = 10) #Typical Low and High Ranges indicated
    
    #Customising presentation of Graph:

        plt.legend()
        plt.xlabel("Days behind from {0}".format(datetime.datetime.utcnow()))
        plt.ylabel("Water level")
    
        plt.xticks(rotation=0) #Can accomodate days number easily on x-axis
        plt.title(station.name)

    # Display plot
        plt.tight_layout()  # This makes sure plot does not cut off date labels

        plt.show()

    

'''Next steps: plot the high and low range as reference lines and label, instead iof points, use itertools.repeat for this to maintian the same value
Consider ideas for how 2G could be done?
'''



#External part of code: required to generate arrays of Station dictionaries, along with dates and level data

stations =  build_station_list()

    # Update latest level data for all stations
update_water_levels(stations)

M = 5 #Selecting 5 stations with hgihest water levels
level_stations = stations_highest_rel_level(stations, M)

dt = 10 #Number of days for levels history
p = 4 #Selecting the maximum order of the polynomial for curve fitting

for station in level_stations:
    dates, levels = fetch_measure_levels(station.measure_id, dt = datetime.timedelta(days = dt))
    plot_water_level_with_fit(station, dates, levels, p)







def testing_polyfit():
    dates = []#Array of datetime objects
    x = mplt.dates.date2num(dates)

# Create set of 10 data points on interval (0, 2)
    x = np.linspace(0, 2, 10)
    y = [0.1, 0.09, 0.23, 0.34, 0.78, 0.74, 0.43, 0.31, 0.01, -0.05]

# Find coefficients of best-fit polynomial f(x) of degree 4
    p_coeff = np.polyfit(x, y, 4) #The higher the order of polynomial, ther greater rthwe accuracy of the curve mapping 

    print(p_coeff)

# Convert coefficient into a polynomial that can be evaluated,
# e.g. poly(0.3)
    poly = np.poly1d(p_coeff) #Can retrun a sequence of coefficients

# Plot original data points
    plt.plot(x, y, '.')

# Plot polynomial fit at 30 points along interval
    x1 = np.linspace(x[0], x[-1], 30)
    plt.plot(x1, poly(x1))

# Display plot
    plt.show()

#testing_polyfit()
