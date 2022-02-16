# Copyright (C) 2018 Garth N. Wells
#
# SPDX-License-Identifier: MIT

from floodsystem.stationdata import build_station_list, update_water_levels
from floodsystem.flood import stations_levels_over_threshold


def run():
    # Build list of stations
    stations = build_station_list()

    # Update latest level data for all stations
    update_water_levels(stations)

    # Check which stations have relative water levels above 0.8
    tol = 0.8

    stations_over_tol = stations_levels_over_threshold(stations, tol)
    for station, level in stations_over_tol:
        print(station.name, level)


if __name__ == "__main__":
    print("*** Task 2B: CUED Part IA Flood Warning System ***")
    run()
