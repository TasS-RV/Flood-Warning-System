from floodsystem.stationdata import build_station_list
from floodsystem.geo import rivers_with_station, stations_by_river, stations_within_radius


def run():
    """Requirements for Task 1D"""

    # Build list of stations
    stations = build_station_list()

    # Get rivers with stations
    rivers = rivers_with_station(stations)

    # Print rivers
    print(f'{len(rivers)} rivers. First 10:', sorted(rivers)[:10])

    # Find stations by river
    stations = stations_by_river(stations)

    # Print stations
    print([station.name for station in stations['River Aire']])
    print([station.name for station in stations['River Cam']])
    print([station.name for station in stations['River Thames']])


if __name__ == "__main__":
    print("*** Task 1D: CUED Part IA Flood Warning System ***")
    run()