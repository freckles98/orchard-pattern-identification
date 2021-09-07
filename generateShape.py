import shapely.coords
from matplotlib import pyplot as plt
from matplotlib.pyplot import plot
from shapely.affinity import affine_transform, translate, rotate
from shapely.geometry import Point, MultiPoint, shape, GeometryCollection
import json
import polygonManipulation as pm
import numpy as np
from matplotlib import pyplot
import sys
from descartes.patch import PolygonPatch
import figures
from scipy.spatial import cKDTree

# from figures import GRAY, BLUE, SIZE, set_limits, plot_line
from shapely.ops import nearest_points


def importData():
    with open("raw_detections2.geojson") as f:
        features = json.load(f)["features"]
    point_set = []
    other_set = []
    for feature in features:
        if feature['properties']['confidence'] > 0.2:
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
    for y in range(range_start_y, end_y,2):
        for x in range(range_start_x, end_x,2):
            point_set.append(Point(x, y))

    if multi_point_bool:
        return MultiPoint(point_set)
    return point_set
# generate set of square

def diamond_set(range_start_x, range_start_y, range_end_x, range_end_y, multi_point_bool):
    point_set = []
    skip = False

    for y in range(range_start_y, range_end_y+range_start_y):

        if (skip == False):
            for x in range(range_start_x, range_end_x+range_start_x, 2):
                point_set.append(Point(x, y))
                skip = True

        else:
            for x in range(range_start_x+1, range_end_x+range_start_x, 2):
                point_set.append(Point(x, y))
                skip = False


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
    data1 = diamond_set(0, 0, 10, 15, False)
    data2 = square_set(10, 0, 10, 15, False)
    data3 = diamond_set(20, 0, 10, 15, False)
    point_set = []
    for x in data1:
        point_set.append(x)

    for y in data2:
        point_set.append(y)

    for z in data3:
        point_set.append(z)

    return to_multipoint(point_set)



def display_data(multi, multi2):
    square_y = []
    square_x = []
    xs = [point.x for point in multi]
    ys = [point.y for point in multi]


    if multi2 != 0:
        xs2 = [point.x for point in multi]
        ys2 = [point.y for point in multi]

        plt.scatter(xs2, ys2, s=1)
        plt.scatter(xs, ys, s=2)
    else:

        plt.scatter(xs, ys, s=1)
    plt.show()

def display_data_pattern(multi):
    square_y = []
    square_x = []
    diamond_x = []
    diamond_y = []
    double_x = []
    double_y = []

    for point in multi:
        print(point.x, point.y, point.hd, point.shape)
        if point.shape == "square":
            square_x.append(point.x)
            square_y.append(point.y)
            print("here")
        if point.shape == "diamond":
            diamond_x.append(point.x)
            diamond_y.append(point.y)
        if point.shape == "double":
            double_x.append(point.x)
            double_y.append(point.y)
    plt.scatter(square_x, square_y, s=1, color='red')
    plt.scatter(diamond_x, diamond_y, s=0.5, color='blue')
    plt.scatter(double_x, double_y, s=0.5, color='yellow')

    plt.show()

def main():
    # data = importData()
    # display_data(data, 0)

    dd = double_row(0, 10, True)
    #display_data(dd, 0)

    # convex = data.minimum_rotated_rectangle
    # display_data(convex)
    # print("convex hull", convex)
    # x, y = convex.exterior.coords.xy
    # print(x, y)

    diamond = diamond_set(0, 0, 5, 10, True)
    #display_data(diamond, 0)
    ms = mixedShape()
    #display_data(ms, 0)


# display_data(diamond)

# print(hausdorff_distance(square_set(0, 10), diamond_set(0, 11)))
# print(hausdorff_distance(square_set(0, 12), square_set(0, 11)))

if __name__ == "__main__":
    main()
    # matching_the_pattern()
# convex = multi_point.convex_hull
# print(convex[0])
# x, y = convex.exterior.coords.xy

# point1 = Point(0, 100)


# point2 = affine_transform(point1, matrix)
# print(f"From {point1.coords.xy} to {point2.coords.xy}")
