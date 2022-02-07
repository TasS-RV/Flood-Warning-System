from floodsystem.geo import rivers_by_station_number, stations_by_river
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





def rivers_by_station_number(stations, N):
    river_stations = [(i[0], len(i[1])) for i in stations_by_river(stations).items()]
    river_stations_sorted = sorted(river_stations, key = lambda x: x[1], reverse = True)

    top_rivers =  []

    for n, r_station in enumerate(river_stations_sorted, 0):
        if n < N-1:
            top_rivers.append(r_station)



        elif n >= N-1:
            if r_station[1] == river_stations_sorted[n+1][1]:
                top_rivers.append(river_stations_sorted[n+1])
            
            elif r_station[1] != river_stations_sorted[n+1][1]:
                break

    return top_rivers 
    

print("\n In new function:")
print(rivers_by_station_number(stations,9))
    
    
    
    
    
    




