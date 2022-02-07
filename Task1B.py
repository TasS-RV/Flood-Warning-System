from floodsystem.stationdata import build_station_list
from floodsystem.geo import stations_by_distance


def run():
    """Requirements for Task 1B"""

    # Geographical coordinates of Cambridge
    cam_coords = (52.2053, 0.1218)

    # Build list of stations
    stations = build_station_list()

    # Get distances (and stations) from Cambridge
    distances = stations_by_distance(stations, cam_coords)

    # Display the ten closest and ten furthest stations
    print("Nearest stations to Cambridge:")
    nearest = [
        (station.name, station.town, distance)
    for station, distance in distances[:10]]
    print(nearest)

    print()
    print("Furthest stations from Cambridge:")
    furthest = [
        (station.name, station.town, distance)
    for station, distance in distances[-10:]]
    print(furthest)


if __name__ == "__main__":
    print("*** Task 1B: CUED Part IA Flood Warning System ***")
    run()