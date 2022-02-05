from itertools import count
from floodsystem.geo import rivers_with_station,stations_by_river
from floodsystem.stationdata import build_station_list
import tkinter

#haversine function - (x1,x2), (y1,y2) - simply computes the distance between them, simple arithmetic calculation

#Obtain the stations for each river, and counnt the number of stations. print the rivers with the largest number of stations

#Dictionary of all stations
stations = build_station_list()





#print(rivers_with_station(stations))
#print(stations_by_river(stations))


river_stations = {}


def func(stations):
    
    for n, station in enumerate(stations_by_river(stations), 0):
        #If River not present in list - adds River, creates list with first count of unique monitoring station
        if station['river'] in river_stations.keys:
            river_stations[station['river']] = [station['Station name']]
    
        else:  #Given unique River key already exists in the dictionary - appends the station into the list
            river_stations[station['river']].append[station['Station name']]

    for n,rs in enumerate(river_stations):
        print(rs)
        if n > 50:
            break     
    return


#func(stations)
print(len(stations_by_river(stations)))


n = 0
for station in stations_by_river(stations).items():
    #river_stations[item] = [s.name for s in r_station]

   

    #print("River name: %s"%item)
    #print('\n')
    #print(stations_by_river(stations)[item])
    #print('\n')
    print(station[0])

    n+=1

    if n>10:
        break



for n, r_station in enumerate(stations_by_river(stations).items(),0):
    river_stations[r_station[0]] = [station.name for station in r_station[1]]

for i in river_stations:
    print(i)







#stations_by_river(stations)  - {'river_name': 'string of stations and info'} ---> split by 'Station name' delimiter into a list of stations
#Count the number of stations of each river - print the highest and lowest counts