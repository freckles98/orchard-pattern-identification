import math

import shapely.coords
from matplotlib import pyplot as plt
from matplotlib.pyplot import plot
from shapely.affinity import affine_transform, translate, rotate
from shapely.geometry import Point, MultiPoint, shape, GeometryCollection
import json
import pyproj
from pyproj import Proj
import polygonManipulation as pm
import numpy as np
from matplotlib import pyplot
import sys
from descartes.patch import PolygonPatch
import figures
from scipy.spatial import cKDTree

# from figures import GRAY, BLUE, SIZE, set_limits, plot_line
from shapely.ops import nearest_points

def determine_ave_confidence(orchard):
    with open(orchard) as f:
        features = json.load(f)["features"]
    ave = 0
    var = 0
    for feature in features:
        ave += feature['properties']['confidence']
    average = ave/len(features)

    for feature in features:
        var += (feature['properties']['confidence'] - average)**2
    std = math.sqrt(var/len(features))
    return average, std


def importData(orchard, ave_confidence):
    with open(orchard) as f:
        features = json.load(f)["features"]
    point_set = []
    other_set = []

    for feature in features:

        if feature['properties']['confidence'] > ave_confidence:
            polygon = feature['geometry']['coordinates'][0]
            polygon_length = len(polygon)
            x = 0
            y = 0
            for coordinate in range(polygon_length):
                x += polygon[coordinate][0]
                y += polygon[coordinate][1]

            x_ave = x / polygon_length
            y_ave = y / polygon_length

            point_set.append(Point(x_ave, y_ave))

        # other_set.append(polygon.centroid) maybe look at using centroid method

    return MultiPoint(point_set), len(features)
    # GeometryCollection([shape(feature["geometry"]).buffer(0) for feature in features])


def square_set(range_start_x, range_start_y, range_end_x, range_end_y, multi_point_bool):
    point_set = []
    end_y = range_end_y+range_start_y
    end_x = range_end_x+range_start_x
    for y in range(range_start_y, end_y):
        for x in range(range_start_x, end_x):
            point_set.append(Point(x, y))

    if multi_point_bool:
        return MultiPoint(point_set)
    return point_set
# generate set of square

def quincunx_set(range_start_x, range_start_y, range_end_x, range_end_y, multi_point_bool):
    point_set = []
    skip = False

    for y in range(range_start_y, range_end_y+range_start_y):


        for x in range(range_start_x, range_end_x+range_start_x):
            point_set.append(Point(x, y))
            x +=0.5
            y +=0.5
            point_set.append(Point(x, y))
            x -= 0.5
            y -= 0.5

    if multi_point_bool:
        return MultiPoint(point_set)
    return point_set


def single_row(range_start_x, range_start_y, range_end_x, range_end_y, multi_point_bool):
    point_set = []
    skip = True

    for y in range(range_start_y, range_end_y + range_start_y):

        for x in range(range_start_x, range_end_x + range_start_x):
            if skip == False:
                point_set.append(Point(x, y))
                skip = True
            else:
                skip = False
            if x== range_end_x+range_start_x-1 and x%2 == 1:
                skip = True


    if multi_point_bool:
        return MultiPoint(point_set)
    return point_set

def double_row(range_start, range_end, multi_point_bool):
    point_set = []
    skip = 0
    for x in range(range_start, range_end):

        if skip != 2:
            for y in range(range_start, range_end):
                point_set.append(Point(x, y))
            skip += 1
        else:
            skip = 0
    if multi_point_bool:
        return MultiPoint(point_set)
    return point_set

def to_multipoint(arr):
    return MultiPoint(arr)

def mixedShape():
    data1 = quincunx_set(0, 0, 10, 15, False)
    data2 = square_set(10, 0, 10, 15, False)
    data3 = quincunx_set(20, 0, 10, 15, False)
    point_set = []
    for x in data1:
        point_set.append(x)

    for y in data2:
        point_set.append(y)

    for z in data3:
        point_set.append(z)

    return to_multipoint(point_set)




def main():
   return

if __name__ == "__main__":
    main()
    # matching_the_pattern()
# convex = multi_point.convex_hull
# print(convex[0])
# x, y = convex.exterior.coords.xy

# point1 = Point(0, 100)


# point2 = affine_transform(point1, matrix)
# print(f"From {point1.coords.xy} to {point2.coords.xy}")
