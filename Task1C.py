from floodsystem.stationdata import build_station_list
from floodsystem.geo import stations_within_radius


def run():
    """Requirements for Task 1C"""

    # Geographical coordinates of Cambridge
    cam_coords = (52.2053, 0.1218)
    radius = 10

    # Build list of stations
    stations = build_station_list()

    # Get stations within 10km from Cambridge
    stations = stations_within_radius(stations, cam_coords, radius)

    # Print stations
    print(sorted([station.name for station in stations]))


if __name__ == "__main__":
    print("*** Task 1C: CUED Part IA Flood Warning System ***")
    run()