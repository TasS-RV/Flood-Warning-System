import matplotlib.pyplot as plt
from matplotlib.dates import date2num
from datetime import datetime, timedelta

from floodsystem.station import MonitoringStation
from floodsystem.plot import plot_water_levels

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

def test_plot_water_levels():

    station = create_test_stations(1)[0]

    dates = [datetime(2016, 12, 30), datetime(2016, 12, 31), datetime(2017, 1, 1),
        datetime(2017, 1, 2), datetime(2017, 1, 3), datetime(2017, 1, 4),
        datetime(2017, 1, 5)]
    levels = [0.2, 0.7, 0.95, 0.92, 1.02, 0.91, 0.64]

    plot, = plot_water_levels(station, dates, levels, show_plot=False)
    x_plot, y_plot = plot.get_xydata().T

    test_dates = [date2num(date) for date in dates]

    assert (x_plot == test_dates).all()
    assert (y_plot == levels).all()


#Can test function: by creating a set of x and y parameters, and checking np.plyfit value agreement rounded to i.e. 1 or 2 dp against the real data
#Test data should be a polynomial itself
#First plot is the real plot for level and dates data, 2nd plot is the polynomial fit plot for reference