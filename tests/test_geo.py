"""Unit test for geo module"""

from random import random
from floodsystem import station

from floodsystem.geo import stations_by_distance, stations_within_radius, rivers_with_station, stations_by_river, rivers_by_station_number
from floodsystem.station import MonitoringStation



def station_create_test(s, s_id, m_id, label, coord, trange, river, town):
    assert s.station_id == s_id
    assert s.measure_id == m_id
    assert s.name == label
    assert s.coord == coord
    assert s.typical_range == trange
    assert s.river == river
    assert s.town == town


def create_test_stations(n):

    # Create n number of stations
    stations = []
    for i in range(n):
        s_id = "s-id-" + str(i)
        m_id = "m-id-" + str(i)
        label = "station" + str(i)
        coord = (i*1.5, i*1.5)
        trange = (-2.3, 3.4445)
        river = "River X"
        town = "My Town"
        s = MonitoringStation(s_id, m_id, label, coord, trange, river, town)

        #Checking station created correctly:
        station_create_test(s, s_id, m_id, label, coord, trange, river, town)
         
  
        stations.append(s) #Adding randomly generated Station into list of stations

    return stations





def test_stations_by_distance():

    stations = create_test_stations(3)

    print(stations)
    p = (2.0, 2.0)
    distances = stations_by_distance(stations, p)

    assert len(distances) == 3
    assert sorted(distances, key=lambda x: x[1]) == distances
    assert type(distances[0][0]) == MonitoringStation
    assert type(distances[1][0]) == MonitoringStation
    assert type(distances[2][0]) == MonitoringStation
    assert type(distances[0][1]) == float
    assert type(distances[1][1]) == float
    assert type(distances[2][1]) == float

def test_stations_within_radius():

    centre = (2.0, 2.0)
    radius = 200

    stations = create_test_stations(3)

    stations = stations_within_radius(stations, centre, radius)

    assert len(stations) == 2
    assert stations[0].station_id == 's-id-1'
    assert stations[1].station_id == 's-id-2'

def test_rivers_with_station():

    stations = create_test_stations(3)
    stations[0].river = 'Nile'
    stations[1].river = 'Nile'
    stations[2].river = 'Rubicon'

    rivers = rivers_with_station(stations)

    assert len(rivers) == 2
    assert 'Nile' in rivers
    assert 'Rubicon' in rivers

def test_stations_by_river():

    stations = create_test_stations(3)
    stations[0].river = 'Nile'
    stations[1].river = 'Nile'
    stations[2].river = 'Rubicon'

    stations_dict = stations_by_river(stations)

    assert len(stations_dict) == 2
    assert len(stations_dict['Nile']) == 2
    assert len(stations_dict['Rubicon']) == 1




def test_rivers_by_station_number():
    stations = create_test_stations(8)
    stations[0].river = "Nile"
    stations[1].river = "Yeongsan"
    stations[2].river = "Yeongsan"
    stations[3].river = "Yeongsan"
    stations[4].river = "Imjin"
    stations[5].river = "Imjin"
    stations[6].river = "Han"
    stations[7].river = "Han"


    river_station = rivers_by_station_number(stations, 3)

    assert river_station[0] == ("Yeongsan", 3)
    assert river_station[1] == ("Imjin", 2) or river_station[1] == ("Han", 2)
    assert river_station[2] == ("Imjin", 2) or river_station[2] == ("Han", 2)
    assert len(river_station) == 3
    # assert river_station[1] == ("Imjin", 4) #These 2 will throw assertion errors
    # assert river_station[0][0] == "Han"

    river_station = rivers_by_station_number(stations, 2)

    assert river_station[0] == ("Yeongsan", 3)
    assert river_station[1] == ("Imjin", 2) or river_station[1] == ("Han", 2)
    assert river_station[2] == ("Imjin", 2) or river_station[2] == ("Han", 2)
    assert len(river_station) == 3