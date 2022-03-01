
import matplotlib.pyplot as plt
from matplotlib.dates import date2num
from datetime import datetime, timedelta
import numpy as np


from floodsystem.station import MonitoringStation
from floodsystem.plot import plot_water_levels, plot_water_level_with_fit

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


def test_plot_water_level_with_fit():

    stations = create_test_stations(6)
    
    #Time history over past 2 days
    dt = 2
   #All stations to have identical datetime ranges  
    day_increments = [timedelta(days = increment) for increment in np.linspace(0, dt ,len(stations))]
    dates = [datetime(2022,2,22) + difference for difference in day_increments] 
    #date2num conversion occurs inside the function itself
    dates_shifted = [(date - date2num(dates)[-1]) for date in date2num(dates)]

    datelevels = {}
    for n, station in enumerate(stations[:-1], 1):
        poly_levels = "(-x-1)**4+(-x-1)**3-(-x-1)**2-(-x-1)+{}".format(str(n))

        #Generates the same polynomial, with a shifted set of levels:
        levels = [eval(poly_levels) for x in dates_shifted]
        datelevels[station.station_id] = [dates, levels]  #This line may not actually be necessary

        station.typical_range = [4,5]#Around midrange of the levels plots
        station.latest_level =  levels[-1] #Most recent level value

        fitted_plot, range_high = plot_water_level_with_fit(station, dates, levels, 4, True, False)

        x = fitted_plot.get_xdata()
        y = fitted_plot.get_ydata()

    #Assertions to check if error between fitted and real values is sufficiently low
        for  real_x, fit_x in zip(dates, x):
        #    print(real_x, fit_x)
            assert (real_x == fit_x)
        
        for  real_y, fit_y in zip(levels, y):
          #  print(real_y, fit_y)
            assert (abs(real_y - fit_y) < 0.0001)
            
        #Testing if high and low ranges are plotted:
        y_range = range_high.get_ydata()
        assert station.typical_range[1] == y_range[1] #Can be any value in the entire list of high range values

    #Testing cases for stations with empty level or dates/ equating to None values
    assert plot_water_level_with_fit(station, [], [], 4, True, False) == "Error: Empty Data Set"
    assert plot_water_level_with_fit(station, None, None, 4, True, False) == "Error: Empty Data Set"


