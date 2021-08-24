import math

import numpy as np
from shapely.geometry import MultiPoint, Point, Polygon
from shapely.ops import nearest_points
from scipy.spatial import distance

import generateShape as gs
# from polygonManipulation import translations
import polygonManipulation as pm


class distances:
    def __init__(self, point_a, point_b, distance):
        self.point_a = point_a
        self.point_b = point_b
        self.distance = distance

    def toStrings(self):
        print(self.point_a, self.point_b, self.distance)


def closest_node(node, nodes):
    nodes = np.asarray(nodes)
    closest_index = distance.cdist([node], nodes).argmin()
    return nodes[closest_index]


def minimise_euclidean_normal(point_set_a, point_set_b):
    distances_set = []
    counter = 0
    for point in point_set_a:
        nearest_geoms = nearest_points(point, point_set_b)
        dist = math.sqrt(((point.x - nearest_geoms[1].x) ** 2) + ((point.y - nearest_geoms[1].y) ** 2))

        if point.x == nearest_geoms[1].x :
            print("Point A: ", point, " Point B: ", nearest_geoms[1])
            print(dist)
        distances_set.append(distances(point, nearest_geoms[1], dist))
        counter += 1
    # for a in point_set_a:
    #     minimum = np.inf
    #     for b in point_set_b:
    #         distance = math.sqrt(((a.x - b.x) ** 2) + ((a.y - b.y) ** 2))
    #
    #         # use early break technique described A. A. Taha and A. Hanbury, “An efficient algorithm for calculating the exact Hausdorff distance.
    #         # instead of 10 maybe use length of model
    #         if distance > 10:
    #             break
    #         #print("a", a, "b", b)
    #         if distance < minimum:
    #             minimum = distance
    #             distances_set[counter] = distances(a, b, distance)
    #             #print(distances_set[counter].point_a, distances_set[counter].point_b, distances_set[counter].distance)
    #             counter += 1

    return distances_set


def find_kth(distance_arr, area):
    maximum = 0
    count = 0
    for x in distance_arr:
        distance = x.distance
        # are the points within an area of matching points
        if (area.contains(x.point_a) or area.touches(x.point_a)) and (
                area.contains(x.point_b) or area.touches(x.point_b)):
            count += 1
            if distance > maximum:
                maximum = distance
    if count == 0:
        return -1
    return maximum


def hausdorff(point_set_a, point_set_b):
    distances_a = minimise_euclidean_normal(point_set_a, point_set_b)

    point_set = []
    # append all distances that are within 0.2 and append them
    for x in distances_a:
        if x.distance < 0.22:
            point_set.append(x.point_a)
    matching_points = MultiPoint(point_set)
    print("Matching points")
    # use minimum rotated rectangle to outline the area of matching points
    area = matching_points.minimum_rotated_rectangle
    print(area)
    distances_b = minimise_euclidean_normal(point_set_b, point_set_a)

    # find the largest separate distance
    max_a = find_kth(distances_a, area)
    max_b = find_kth(distances_b, area)

    if max_a > max_b:
        return max_a
    return max_b


def main():
    square = gs.square_set(2, 6)
    square2 = gs.diamond_set(0, 2)
    gs.display_data(square, square2)
    square2 = pm.translations(square2, 0.5, 0)
    print("Hausdorff distance: ", hausdorff(square, square2))


if __name__ == "__main__":
    main()
