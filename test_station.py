"""Unit test for the station module"""

from datetime import datetime, timedelta
import numpy as np
from floodsystem.station import MonitoringStation
from floodsystem.station import inconsistent_typical_range_stations


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
        trange = (5, 25)
        river = "River X"
        town = "My Town"
        s = MonitoringStation(s_id, m_id, label, coord, trange, river, town)

        #Checking station created correctly:
        station_create_test(s, s_id, m_id, label, coord, trange, river, town)

        stations.append(s) #Adding randomly generated Station into list of stations

    return stations



def test_inconsistent_typical_range_stations():

    stations = create_test_stations(5)
    
    #Above redundant - main part required for test
    stations[0].typical_range = None
    stations[1].typical_range = [4.0,1.0]
    stations[2].typical_range = [3.0,2.0]

    inconsistent_stations = inconsistent_typical_range_stations(stations)

    assert inconsistent_stations == ['station0','station1','station2']
    assert stations[0].typical_range_consistent() == False
    assert stations[4].typical_range_consistent() == True   #Tests True/ False if stations are Consistent/ Inconsistent respectively
    
  # assert stations[4].typical_range_consistent == False
   #assert inconsistent_stations == ['station0','station1','station4']
 
#Checking:
#print(test_inconsistent_typical_range_stations())

def test_relative_water_level():
    station = create_test_stations(1)[0]

    station.latest_level = 10

    assert station.relative_water_level() == 0.25