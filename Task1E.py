from floodsystem.geo import rivers_by_station_number
from floodsystem.stationdata import build_station_list


#Obtain the stations for each river, and counnt the number of stations. print the rivers with the largest number of stations

#Dictionary of all stations
stations = build_station_list()

N = 9#Top N number of rivers with highest number of stations

def runE(stations, N):
    return rivers_by_station_number(stations, N)



if __name__ == "__main__":
    runE(stations, N)
    print(runE(stations, N))



