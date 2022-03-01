


import matplotlib.pyplot as plt
from matplotlib.dates import date2num
from datetime import datetime, timedelta
import numpy as np


from floodsystem.station import MonitoringStation
from floodsystem.flood import risk_assessment




def test_risk_assessment():

    stations = create_test_stations(10)
    
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
        
        y_range = range_high.get_ydata()
        assert station.typical_range[1] == y_range[1] #Can be any value in the entire list of high range values

    #Testing cases for stations with empty level or dates/ equating to None values
    assert plot_water_level_with_fit(station, [], [], 4, True, False) == "Error: Empty Data Set"
    assert plot_water_level_with_fit(station, None, None, 4, True, False) == "Error: Empty Data Set"

    risk_level = {}
    if levels != None and len(dates) > 0:
            risk_level[station.town] = risk_assessment(station, dates, levels, 4, False)

    
    



        