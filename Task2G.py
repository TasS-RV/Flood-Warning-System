from difflib import context_diff
from floodsystem.datafetcher import fetch_measure_levels
from floodsystem.flood import stations_highest_rel_level
from floodsystem.stationdata import build_station_list, update_water_levels
from floodsystem.plot import plot_water_level_with_fit

import datetime
from matplotlib import pyplot as plt
import matplotlib as mplt
import numpy as np


#Consider algorthm 
#Using relative data for a scaled number
#Multiplier of 0.6
#Multiplier of 0.4: using extrapolatio, using derivative from polynomial function
#Predict tomorrows: 0.4x tomorrow + 0.6x todays
#/2 for the relative value, and thresholds applied

#How to test? Known value of station that would be low, high, moderate etc... (4 tests)
#Then check if it returns the correct reading
#Use the same range of dates but different functions


#Loops runs once per station: station object, array of levels and timestamps (dates)

def risk_assessment(station, dates, levels, p):

    date_count = mplt.dates.date2num(dates)
    date_count_shifted = [day - date_count[0] for day in date_count]
    
    #Value given relative to typical High value: shifted by Low value
    rel_levels  = [level/(station.typical_range[1] - station.typical_range[0]) for level in levels]
    
    coeff = np.polyfit(date_count_shifted, rel_levels, p)  #Coefficient finding for fitting level and dates data with polynomial or degree p
    fitted_levels = np.poly1d(coeff) #Y-values for polynomial fit relative to correcponding x values of date_count_shifted

    #Linearisation performed with time-step 1 (equivalent to 1 day)
    #eval(.format((date_count_shifted[-1]+1),))

    coeff_series = [c for c in coeff]
    coeff_series.reverse() #To reverse in order of increasing exponents

    func = ""
    for expo, c in enumerate(coeff_series, 0): #Last coeff. is constant term, equivalent to x^0
        func = func + str(c) + "*(x**{})*".format(expo)
    func = func + "1" #Due to extra * at end
    
    deriv = ""
    #Can apply algorithmic differentiation method for polynomial:
    for expo, c in enumerate(coeff_series[1:], 1): #Last coeff. is constant term, equivalent to x^0
        deriv = deriv + str(c*expo) + "*(x**{})*".format(expo-1)
    deriv = deriv + "1"
    
    #Presenting functions for testing:
    print("\n Normal function: {}".format(func))
    print("Derivative of function: {}".format(deriv))

    #[eval(deriv) for x in rel_levels] generates a list of values
    plt.plot(date_count_shifted, rel_levels, color = 'b', label = "True values")
    plt.plot(date_count_shifted, fitted_levels, color = 'r', label = "Fitted values") #Values with polynomial
  #  x = date_count_shifted[-1]+1 #Next day increment
   # date_count_shifted.append(x)
    
    #.append(fitted_levels[-1]+1*int(eval(deriv))) #Linearised next value of water level 

  #  plt.plot(date_count_shifted, fitted_levels, color = 'r') #Values with polynomial 
   # plt.plot(date_count_shifted, [eval(deriv) for x in rel_levels])

    plt.legend()
    plt.show()

    #Scaling factors based on relative importance of present (ps) and tomorrow's level data (fs) 
    ps = 0.6
    fs = 0.4 

    



def task_run():    
    stations =  build_station_list()

    # Update latest level data for all stations (to present time))
    update_water_levels(stations)

    dt = 3 #Number of days for levels history - too high and polyfit may not be accurate, too low and insufficient points
    p = 4 #Selecting the maximum order of the polynomial for curve fitting
    
    #Dictioanry of towns followed by numerical risk scaling (discrete)
    risk_level = {}

    for station in stations:
        dates, levels = fetch_measure_levels(station.measure_id, dt = datetime.timedelta(days = dt))
  
        risk_level[station.town] = risk_assessment(station, dates, levels, p)



if __name__ == "__main__":
    task_run()