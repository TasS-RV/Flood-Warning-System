from floodsystem.geo import rivers_with_station
from floodsystem.stationdata import build_station_list


#In station, MonitoringStation class, method that compares the values of high and low ranges
#returns true if consistent, false if inconsistent

#Use that method, check the False stations accumulate into a list in the inconsistent_typical_range_stations functions