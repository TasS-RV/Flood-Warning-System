from floodsystem.datafetcher import fetch_measure_levels
from floodsystem.flood import stations_highest_rel_level
from floodsystem.stationdata import build_station_list, update_water_levels
from floodsystem.plot import plot_water_level_with_fit


#Consider algorthm 
#Using relative data for a scaled number
#Multiplier of 0.6
#Multiplier of 0.4: using extrapolatio, using derivative from polynomial function
#Predict tomorrows: 0.4x tomorrow + 0.6x todays
#/2 for the relative value, and thresholds applied

#How to test? Known value of station that would be low, high, moderate etc... (4 tests)
#Then check if it returns the correct reading
#Use the same range of dates but different functions