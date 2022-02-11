from .station import MonitoringStation

def stations_levels_over_threshold(stations, tol):
    output = []
    for station in stations:
        rel_level = station.relative_water_level()
        try:
            if rel_level > tol:
                output.append((station, station.relative_water_level()))
        except:
            pass
    return sorted(output, key=lambda x: x[0].relative_water_level(), reverse=True)