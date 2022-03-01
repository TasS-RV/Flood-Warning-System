"""Unit test for flood module"""

import matplotlib.pyplot as plt
from matplotlib.dates import date2num
from datetime import datetime, timedelta
import numpy as np



from floodsystem.station import MonitoringStation
from floodsystem.flood import stations_levels_over_threshold, stations_highest_rel_level
import datetime
from floodsystem.flood import risk_assessment

"""Does not appear to work when I place the test_risk_assessment files into this test file, or these tests into the test_2g file - either way 'module' object is not callable turns up"""


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






#Shifted graphs of individual stations were plotted, and linearation performed and weighting risk factor calculated to determine the Flood Risk and Water level rising/ falling state"

def risk_assertions(station, risk, state):
    if station.town == "Town 0":
        assert (risk == "LOW", state == "Falling")
    
    elif station.town == "Town 1":
        assert (risk == "LOW", state == "Rising")
    
    elif station.town == "Town 5":
        assert (risk == "MODERATE", state == "Rising")
    
    elif station.town == "Town 6":
        assert (risk == "MODERATE", state == "Falling")
    
    elif station.town == "Town 7":
        assert (risk == "HIGH", state == "Rising")
    
    elif station.town == "Town 8":
        assert (risk == "HIGH", state == "Falling")
    
    elif station.town == "Town 9":
        assert (risk == "SEVERE", state == "Rising")
    
    else: 
        pass
    


#Testing main fucntionality for 2G:
def test_risk_assessment():

    stations = create_test_stations(10)
    
    #Time history over past 2 days
    dt = 2
   #All stations to have identical datetime ranges  
    day_increments = [timedelta(days = increment) for increment in np.linspace(0, dt ,len(stations))]
    dates = [datetime(2022,2,22) + difference for difference in day_increments] 
    #date2num conversion occurs inside the function itself
    dates_shifted = [(date - date2num(dates)[-1]) for date in date2num(dates)]

    risk_level = {}

    for n, station in enumerate(stations, 1):
        if n%2 == 0:
            poly_levels = "(-x-1)**4+(-x-1)**3-(-x-1)**2-(-x-1)+{}".format(str(n))
        else:
            poly_levels = "(-x-1.3)**4+(-x-1.3)**3-(-x-1.3)**2-(-x-1.3)+{}".format(str(n))

        #Generates the same polynomial, with a shifted set of levels:
        levels = [eval(poly_levels) for x in dates_shifted]
        station.typical_range = [5,7]#Around midrange of the levels plots
        station.latest_level =  levels[-1] #Most recent level value
        station.town = town = "Town {}".format(n-1)

        risk_level[station.town] = risk_assessment(station, dates, levels, 4, False)
        
        #Assertions only from a selection of stations to test each and combination of risk:
        risk_assertions(station, risk_level[station.town][0],  risk_level[station.town][1])


