from floodsystem.geo import stations_by_river
from floodsystem.stationdata import build_station_list
import itertools

#haversine function - (x1,x2), (y1,y2) - simply computes the distance between them, simple arithmetic calculation

#Obtain the stations for each river, and counnt the number of stations. print the rivers with the largest number of stations

#Dictionary of all stations
stations = build_station_list()


def rivers_by_station_number(stations, N):
    stations_count = []
   # river_stations = {}
    
    for n, r_station in enumerate(stations_by_river(stations).items(),0):
       # river_stations[r_station[0]] = [station.name for station in r_station[1]]  #Redundant -  Dictionary of Rivers, with list of Station names affiliated
       stations_count.append((r_station[0], len(r_station[1]))) #Tuple containing Number if Stations and River names

    stations_sorted = sorted(stations_count, key = lambda entry: entry[1], reverse= True) #2nd values stores the number of rivers 
    stations_sorted_dict = {}
    #print(stations_sorted)

    for ind, station in enumerate(stations_sorted,0):
       
        if ind > N:
            if stations_sorted[ind+1][1] == station[1]:  #If overflowing - due to 'tie' in number of stations
                stations_sorted_dict[str(station[1])].append(stations_sorted[ind+1][0]) #Adds River entry
            else:
                break #Once required number of RIvers obtained/ exceeded - stops accumulating

        elif ind <= N:
            if str(station[1]) not in stations_sorted_dict.keys():
                stations_sorted_dict[str(station[1])]  = [station[0]] #Adds River name to dicitonary of Rivers with keys as their number of Monitoring Stations
            
            else:
                stations_sorted_dict[str(station[1])].append(station[0])
    rs_output = []
    
    #Reconversion back into list of tuples: (River, Number of Stations assigned to River)
    for number, rivers in stations_sorted_dict.items():
        for r in rivers:
            rs_output.append((r, int(number)))

    return rs_output

#print(rivers_by_station_number(stations, 9))
