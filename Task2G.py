from difflib import context_diff
from floodsystem.datafetcher import fetch_measure_levels
from floodsystem.flood import stations_highest_rel_level
from floodsystem.stationdata import build_station_list, update_water_levels
from floodsystem.station import inconsistent_typical_range_stations, MonitoringStation


import datetime
from matplotlib import pyplot as plt
import matplotlib as mplt
import numpy as np
from itertools import groupby

#Arbitrarily decided thresholds: 1 - Low, 2 - Moderate, 3 - High, 4 - Severe (Risk levels for flooding)

def risk_threshold(relative_scale):
    low = 0.0
    moderate = 0.94
    high = 1.9

    if relative_scale <= low:
        return 1
    elif low < relative_scale <= moderate:
        return 2
    elif moderate < relative_scale <= high:
        return 3
    elif relative_scale > high:
        return 4
     
#Loops runs once per station: station object, array of levels and timestamps (dates)

def risk_assessment(station, dates, levels, p, plot = False):

    date_count = mplt.dates.date2num(dates)
    date_count_shifted = [day - date_count[-1] for day in date_count]
    date_count_shifted.reverse()
    
    if levels != None: #Checking for non-empty list

        try:


                
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
                func = func + str(c) + "*(x**{})+".format(expo)
            func = func + "0" #Due to extra  at end
            
            deriv = ""
            #Can apply algorithmic differentiation method for polynomial:
            for expo, c in enumerate(coeff_series[1:], 1): #Last coeff. is constant term, equivalent to x^0
                deriv = deriv + str(c*expo) + "*(x**{})+".format(expo-1)
            deriv = deriv + "0"
            #Presenting functions for testing:#print("\n Normal function: {}".format(func))#print("Derivative of function: {}".format(deriv))
            
            
            #Linearisation:
            rel_levels_fitted = list(fitted_levels(date_count_shifted))#np.array must be converted into list for append function use
            x = date_count_shifted[-1] #Present day value


            #Pre-linearisation graphs:
            if plot == True:
            #[eval(deriv) for x in rel_levels] generates a list of values
                plt.plot(date_count_shifted, rel_levels, color = 'b', label = "True values")
                plt.plot(date_count_shifted, rel_levels_fitted, color = 'r', label = "Fitted values") #Values with polynomial


            #1/4 day value
            quarter_day = rel_levels_fitted[-1] + eval(deriv)*0.25
            date_count_shifted.append(x+0.25)
            #1/2 Day value
            half_day = rel_levels_fitted[-1] + eval(deriv)*0.5
            date_count_shifted.append(x+0.5)

            rel_levels_fitted.append(quarter_day) #Using rate of change at present 
            rel_levels_fitted.append(half_day)
            
            #Graphical display of predicted water level:
            if plot == True:
                plt.plot(date_count_shifted, rel_levels_fitted, color = 'g', label = "Linearised next value") #Values with polynomial 
            # plt.plot(date_count_shifted, [eval(deriv) for x in rel_levels], color = 'o', label = "First derivative of fitted polynomial")
                plt.xlabel("Days TO present from 3 days ago")
                plt.ylabel("Relative water level to typical range values.")
            
                plt.title(station.town)
                plt.legend()
                plt.show()

            #Scaling factors based on relative importance of present (ps) and quarter day (fs1) and half day (fs2)
            ps = 0.55
            fs1 = 0.33 
            fs2 = 0.12
            
            relative_scale = ps*rel_levels_fitted[-3] + fs1*quarter_day + fs2*half_day
            return risk_threshold(relative_scale)
        
        except Exception:
            print(station, levels, dates)





def task_run(show_plot):    
    stations =  build_station_list()

    consistent_stations = [station for station in stations if station.name not in inconsistent_typical_range_stations(stations)]
     
    #Reusing this as invalid stations are prefiltered out
    M = len(stations)
    consis_stations = stations_highest_rel_level(stations, M)
   
    # Update latest level data for all stations (to present time))
    update_water_levels(stations)
    
    #Uncomment out for refernce to typical scales of Highest and Lowest Water level stations
   # M = 5 #Selecting 5 stations with hgihest water levels
    #high_stations = stations_highest_rel_level(stations, M)

    
    dt = 3 #Number of days for levels history - too high and polyfit may not be accurate, too low and insufficient points
    p = 4 #Selecting the maximum order of the polynomial for curve fitting
    
    #Dictioanary of towns followed by numerical risk scaling (discrete)
    risk_level = {}

    for station in consis_stations:
        dates, levels = fetch_measure_levels(station.measure_id, dt = datetime.timedelta(days = dt))
        risk_level[station.town] = risk_assessment(station, dates, levels, p, show_plot)
        
        if risk_level[station.town] == None:
            print(station.name)
            print(levels)
            print(dates)
        
       # print(risk_level)
    
        
        
   # for key, group in groupby(risk_level, lambda x: risk_level[x]):
    #    print(key, group)


if __name__ == "__main__":
    show_plot = False
    task_run(show_plot)