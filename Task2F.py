import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mplt
import datetime
from floodsystem.datafetcher import fetch_measure_levels

from floodsystem.flood import stations_highest_rel_level
from floodsystem.stationdata import build_station_list, update_water_levels
from floodsystem.plot import plot_water_levels, testing_polyfit







stations =  build_station_list()

# Update latest level data for all stations
update_water_levels(stations)

M = 5 #Selecting 5 stations with hgihest water levels
level_stations = stations_highest_rel_level(stations, M)

dt = 10 #Number of days for levels history

for station in level_stations:
    dates, levels = fetch_measure_levels(station.measure_id, dt = datetime.timedelta(days = dt))
    plot_water_levels(station, dates, levels)
    

testing_polyfit()

def plot_water_level_with_fit(station, dates, levels, p):
    pass




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
