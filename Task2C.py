# Copyright (C) 2018 Garth N. Wells
#
# SPDX-License-Identifier: MIT

from floodsystem.stationdata import build_station_list, update_water_levels
from floodsystem.flood import stations_highest_rel_level


def run():
    # Build list of stations
    stations = build_station_list()

    # Update latest level data for all stations
    update_water_levels(stations)

    # Get the 10 stations with the highest relative levels
    N = 10
    stations = stations_highest_rel_level(stations, N)

    for station in stations:
        print(station.name, station.relative_water_level())

    # Alternative implementation
    # for station in [s for s in stations if s.name in names]:
    #     print("Station name and current level: {}, {}".format(station.name,
    #                                                           station.latest_level))


if __name__ == "__main__":
    print("*** Task 2C: CUED Part IA Flood Warning System ***")
    run()
