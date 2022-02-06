from floodsystem.station import inconsistent_typical_range_stations
from floodsystem.stationdata import build_station_list 

#Building list of station objects
stations = build_station_list()

def runF(stations):
    return inconsistent_typical_range_stations(stations)



if __name__ == "__main__":
    runF(stations)
    #print(runF(stations))

