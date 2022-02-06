from floodsystem.geo import stations_by_river
from floodsystem.stationdata import build_station_list 
from floodsystem.station import MonitoringStation


stations = build_station_list()

def inconsistent_typical_range_stations(stations):
    count =  0

    


    for station in stations:
        count+=1
        print(station.typical_range)
        print('\n')
        print(station)
        print('\n')
        
         
        if station.typical_range == None:
            print("False")

        elif station.typical_range[0] < station.typical_range[1]:
            print("True")
        
        elif station.typical_range[0] > station.typical_range[1]:
            print("False")

        if count>= 100:
            break


print(inconsistent_typical_range_stations(stations))


#In station, MonitoringStation class, method that compares the values of high and low ranges
#returns true if consistent, false if inconsistent

#Use that method, check the False stations accumulate into a list in the inconsistent_typical_range_stations functions