"""Unit test for flood module"""

from floodsystem.station import MonitoringStation
from floodsystem.flood import stations_levels_over_threshold, stations_highest_rel_level

def create_test_stations(n):

    # Create n number of stations
    stations = []
    for i in range(n):
        s_id = "s-id-" + str(i)
        m_id = "m-id-" + str(i)
        label = "station" + str(i)
        coord = (i*1.5, i*1.5)
        trange = (0, 10)
        river = "River X"
        town = "My Town"
        s = MonitoringStation(s_id, m_id, label, coord, trange, river, town)
         
  
        stations.append(s) #Adding randomly generated Station into list of stations

    return stations

def test_stations_level_over_threshold():

    threshold = 0.7

    stations = create_test_stations(7)
    stations[0].latest_level = None # Test unavailable data
    stations[1].latest_level = 9
    stations[2].latest_level = 7
    stations[3].latest_level = 4
    stations[4].latest_level = 8
    stations[5].latest_level = 9.5
    stations[6].latest_level = 9
    
    stations[1].typical_range = (2, 1)  # Test inconsistent range data

    result = stations_levels_over_threshold(stations, threshold)

    assert result == sorted(result, key=lambda x: x[0].relative_water_level(), reverse=True)
    assert len(result) == 3
    assert [level for station, level in result] == [0.95, 0.9, 0.8]

def test_stations_highest_rel_level():
    
    stations = create_test_stations(7)
    stations[0].latest_level = None # Test unavailable data
    stations[1].latest_level = 9
    stations[2].latest_level = 7
    stations[3].latest_level = 4
    stations[4].latest_level = 8
    stations[5].latest_level = 9.5
    stations[6].latest_level = 9
    
    stations[1].typical_range = (2, 1)  # Test inconsistent range data

    result = stations_highest_rel_level(stations, 4)


    assert result == sorted(result, key=lambda x: x.relative_water_level(), reverse=True)
    assert len(result) == 4
    assert result[0]  == stations[5]
    assert result[1]  == stations[6]
    assert result[2]  == stations[4]
    assert result[3]  == stations[2]