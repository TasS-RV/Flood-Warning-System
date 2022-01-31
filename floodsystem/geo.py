# Copyright (C) 2018 Garth N. Wells
#
# SPDX-License-Identifier: MIT
"""This module contains a collection of functions related to
geographical data.

"""

from .utils import sorted_by_key  # noqa
from haversine import haversine
from .station import MonitoringStation

def stations_by_distance(stations, p):
    return sorted([
        (station, haversine(station.coord, p))
    for station in stations], key=lambda x: x[1])

def stations_within_radius(stations, centre, r):
    return [station for station in stations if haversine(station.coord, centre) <= r]