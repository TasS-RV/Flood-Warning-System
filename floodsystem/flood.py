from .station import MonitoringStation
from matplotlib import pyplot as plt
import matplotlib as mplt
import numpy as np


def stations_levels_over_threshold(stations, tol):
    output = []
    for station in stations:
        rel_level = station.relative_water_level()
        try:
            if rel_level > tol:
                output.append((station, station.relative_water_level()))
        except:
            pass
    return sorted(output, key=lambda x: x[0].relative_water_level(), reverse=True)

def stations_highest_rel_level(stations, N):
    stations = [station for station in stations if station.relative_water_level() != None and station.relative_water_level() <= 50]
    return sorted(stations, key=lambda x: x.relative_water_level(), reverse=True)[:N]
  #  return sorted(stations, key=lambda x: x.relative_water_level(), reverse=False)[:N]
  # ^ Used as a reference test to see if the top 5 station water levels were feasible: as significantly higher than the typical range High


#Functions for Task 2G:

#Arbitrarily decided thresholds: 1 - Low, 2 - Moderate, 3 - High, 4 - Severe (Risk levels for flooding)
def risk_threshold(relative_scale):
    low = 0.0
    moderate = 0.94
    high = 1.9

    if relative_scale <= low:
        return "LOW"
    elif low < relative_scale <= moderate:
        return "MODERATE"
    elif moderate < relative_scale <= high:
        return "HIGH"
    elif relative_scale > high:
        return "SEVERE"
     
#Gives predicted state of water level: if rising or falling or stagnating
def level_state(gradient):
    if gradient > 0:
        return "Rising"
    elif gradient == 0:
        return "Stagnating"
    elif gradient < 0:
        return "Falling"
    
    


#Loops runs once per station: station object, array of levels and timestamps (dates)

def risk_assessment(station, dates, levels, p, plot = False):

    date_count = mplt.dates.date2num(dates)
    date_count_shifted = [day - date_count[-1] for day in date_count]
    date_count_shifted.reverse()
    

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
    
    #Current rate of change
    grad_today = eval(deriv)

    #1/4 day value
    quarter_day = rel_levels_fitted[-1] + grad_today*0.25
    date_count_shifted.append(x+0.25)
    #1/2 Day value
    half_day = rel_levels_fitted[-1] + grad_today*0.5
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
    return risk_threshold(relative_scale), level_state(grad_today)
    