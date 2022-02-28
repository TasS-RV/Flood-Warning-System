import matplotlib
import matplotlib.pyplot as plt
from matplotlib.dates import date2num
from datetime import datetime, timedelta
import numpy as np


from floodsystem.station import MonitoringStation
from floodsystem.plot import plot_water_levels, plot_water_level_with_fit
from floodsystem.flood import stations_highest_rel_level

def station_create_test(s, s_id, m_id, label, coord, trange, river, town):
    assert s.station_id == s_id
    assert s.measure_id == m_id
    assert s.name == label
    assert s.coord == coord
    assert s.typical_range == trange
    assert s.river == river
    assert s.town == town


def create_test_stations(n):

    # Create n number of stations
    stations = []
    for i in range(n):
        s_id = "s-id-" + str(i)
        m_id = "m-id-" + str(i)
        label = "station" + str(i)
        coord = (i*1.5, i*1.5)
        trange = (5, 25)
        river = "River X"
        town = "My Town"
        s = MonitoringStation(s_id, m_id, label, coord, trange, river, town)

        #Checking station created correctly:
        station_create_test(s, s_id, m_id, label, coord, trange, river, town)

  
        stations.append(s) #Adding randomly generated Station into list of stations

    return stations

def test_plot_water_levels():

    station = create_test_stations(1)[0]

    dates = [datetime(2016, 12, 30), datetime(2016, 12, 31), datetime(2017, 1, 1),
        datetime(2017, 1, 2), datetime(2017, 1, 3), datetime(2017, 1, 4),
        datetime(2017, 1, 5)]
    levels = [0.2, 0.7, 0.95, 0.92, 1.02, 0.91, 0.64]

    plot, = plot_water_levels(station, dates, levels, show_plot=False)
    x_plot, y_plot = plot.get_xydata().T

    test_dates = [date2num(date) for date in dates]

    assert (x_plot == test_dates).all()
    assert (y_plot == levels).all()


#Can test function: by creating a set of x and y parameters, and checking np.plyfit value agreement rounded to i.e. 1 or 2 dp against the real data
#Test data should be a polynomial itself
#First plot is the real plot for level and dates data, 2nd plot is the polynomial fit plot for reference


def test_plot_water_level_with_fit():
    stations = create_test_stations(10)
    
    #c is the offset of the function
    poly_levels = "(-x-1)**4+(-x-1)**3-(-x-1)**2-(-x-1)+1"
    dt = 2

    day_increments = [timedelta(days = increment) for increment in np.linspace(0, dt ,len(stations))]
    dates = [datetime(2022,2,22) + difference for difference in day_increments] 
    
    #date2num conversion occurs inside the function itself
    dates_counted = date2num(dates)
    dates_shifted = [(date - dates_counted[-1]) for date in dates_counted]
    levels = [eval(poly_levels) for x in dates_shifted]

    p = 4
    coeff = np.polyfit(dates_shifted, levels, p)  #Coefficient finding for fitting level and dates data with polynomial or degree p
    # Convert coefficient into a polynomial that can be evaluated
    poly = np.poly1d(coeff)
    
    #Polyfit does appear to get the points exactly
    fitted_plot, = plt.plot(dates_shifted, poly(dates_shifted), color = 'b', label = "Best-fit Curve")
    plt.plot(dates_shifted, levels, color = 'r')
    
    x = fitted_plot.get_xdata().T
    y = fitted_plot.get_ydata().T
    #plt.show()
    
    # Throws: ValueError: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()
    # If attempting to check equality between array objects on their own - without specifying number
    #assert (x == dates_shifted).all()
    #assert (y == levels).all()
    
    print(y)
    print('\n\n')
    print(levels)
    #for i in range(1,len(station)+1):




    M = 5 #Selecting 5 stations with highest water levels
    level_stations = stations_highest_rel_level(stations, M)

    p = 4 #Selecting the maximum order of the polynomial for curve fitting
    range_plot = False #True/False to plot high and low water level lines

 #   for station in level_stations:
  #      dates, levels = fetch_measure_levels(station.measure_id, dt = datetime.timedelta(days = dt))
   #     plot_water_level_with_fit(station, dates, levels, p, range_plot)  



test_plot_water_level_with_fit()