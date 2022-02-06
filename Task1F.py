from floodsystem.geo import stations_by_river
from floodsystem.stationdata import build_station_list 



stations = build_station_list()

def inconsistent_typical_range_stations(stations):
    count =  0

    


    for station in stations:
        count+=1
        print(station)
        print('\n')
        print(station.typical_range)
        print('\n')
        print(station.typical_range_consistent)

        if count>= 10:
            break

        


print(inconsistent_typical_range_stations(stations))


#In station, MonitoringStation class, method that compares the values of high and low ranges
#returns true if consistent, false if inconsistent

#Use that method, check the False stations accumulate into a list in the inconsistent_typical_range_stations functions