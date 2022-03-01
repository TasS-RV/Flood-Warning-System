
import matplotlib.pyplot as plt
from matplotlib.dates import date2num
from datetime import datetime, timedelta
import numpy as np


from floodsystem.station import MonitoringStation
from floodsystem.flood import risk_assessment
from floodsystem.flood import stations_levels_over_threshold, stations_highest_rel_level


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

 





