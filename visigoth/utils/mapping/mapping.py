# -*- coding: utf-8 -*-

#    visigoth: A lightweight Python3 library for rendering data visualizations in SVG
#    Copyright (C) 2020  Niall McCarroll
#
#   Permission is hereby granted, free of charge, to any person obtaining a copy of this software
#   and associated documentation files (the "Software"), to deal in the Software without
#   restriction, including without limitation the rights to use, copy, modify, merge, publish,
#   distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the
#   Software is furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included in all copies or
#   substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
#   BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
#   NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#   DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import math
from visigoth.utils.mapping.projections import Projections

class Mapping(object):

    def __init__(self):
        pass

    """
    Compute the bounding box around a given center point 

    Arguments:
        center(tuple): the center coordinares as a (lon,lat) pair
        radius(int): the radius (in metres) around the center to display
        projection(object): the projection system to use
        
    Returns:
        boundaries(tuple): tuple containing (min-lon,min-lat) and (max-lon,max-lat) pairs   
    """
    @staticmethod
    def computeBoundaries(center,distance,projection=Projections.EPSG_3857):

        # based on:
        # https://github.com/jfein/PyGeoTools/blob/master/geolocation.py
        # and:
        # http://janmatuschek.de/LatitudeLongitudeBoundingCoordinates

        radius = 6372800  # Approx Earth radius in meters

        # angular distance in radians on a great circle
        rad_dist = distance / radius

        MIN_LAT = math.radians(-90)
        MAX_LAT = math.radians(90)
        MIN_LON = math.radians(-180)
        MAX_LON = math.radians(180)

        (deg_lon,deg_lat) = center
        rad_lat = math.radians(deg_lat)
        rad_lon = math.radians(deg_lon)

        min_lat = rad_lat - rad_dist
        max_lat = rad_lat + rad_dist

        if min_lat > MIN_LAT and max_lat < MAX_LAT:
            delta_lon = math.asin(math.sin(rad_dist) / math.cos(rad_lat))

            min_lon = rad_lon - delta_lon
            if min_lon < MIN_LON:
                min_lon += 2 * math.pi

            max_lon = rad_lon + delta_lon
            if max_lon > MAX_LON:
                max_lon -= 2 * math.pi
        else:
            min_lat = max(min_lat, MIN_LAT)
            max_lat = min(max_lat, MAX_LAT)
            min_lon = MIN_LON
            max_lon = MAX_LON

        return ((math.degrees(min_lon),math.degrees(min_lat)),(math.degrees(max_lon),math.degrees(max_lat)))

    """
    Compute the bounding box around a set of locations 

    Arguments:
        locations(list): list of (lon,lat) pairs
        fraction of the locationarea to use as a margin 

    Returns:
        boundaries(tuple): tuple containing (min-lon,min-lat) and (max-lon,max-lat) pairs   
    """
    @staticmethod
    def getBoundingBox(locations,fraction):
        lat_min = min([lat for (_,lat) in locations])
        lat_max = max([lat for (_,lat) in locations])
        lon_min = min([lon for (lon,_) in locations])
        lon_max = max([lon for (lon,_) in locations])
        lat_range = lat_max - lat_min
        lon_range = lon_max - lon_min
        if not lat_range:
            lat_range = 0.1
        if not lon_range:
            lon_range = 0.1 
        lat_min -= lat_range*fraction
        lat_max += lat_range*fraction
        lon_min -= lon_range*fraction
        lon_max += lon_range*fraction
        
        return ((lon_min,lat_min),(lon_max,lat_max))

    """
    Compute the haversine (great circle) distance between two (lon,lat) points 

    Arguments:
        lonlat1: first point expressed as (lon,lat) tuple
        lonlat2: second point expressed as (lon,lat) tuple
        
    Returns:
        approximate distance between two points   
    """
    @staticmethod
    def haversine(lonlat1,lonlat2):
        # based on https://rosettacode.org/wiki/Haversine_formula#Python
        lon1 = lonlat1[0]
        lat1 = lonlat1[1]
        lon2 = lonlat2[0]
        lat2 = lonlat2[1]

        R = 6372800  # Approx Earth radius in meters

        dLat = math.radians(lat2 - lat1)
        dLon = math.radians(lon2 - lon1)
        lat1 = math.radians(lat1)
        lat2 = math.radians(lat2)

        a = math.sin(dLat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dLon / 2)**2
        c = 2 * math.asin(math.sqrt(a))

        return R * c


