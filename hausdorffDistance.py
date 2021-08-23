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
    print("start of euclid")
    distances_set = [0] * len(point_set_a)
    counter = 0
    for point in point_set_a:

         nearest_geoms = nearest_geoms(point, point_set_b)
         print(nearest_geoms)
         distance = math.sqrt(((point.x - nearest_geoms[1].x) ** 2) + ((point.y - nearest_geoms[1].y) ** 2))
         distances_set[counter] = distances(point, nearest_geoms[1], distance)
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

    # for i in range(len(distances_set)):
    # print(distances_set[i].toStrings())
    print("end of euclid")

    return distances_set


def find_kth(distance_arr, area):
    print("start of kth")
    maximum = 0
    count = 0
    for x in range(len(distance_arr)):
        if hasattr('abc','distance') == False:
            break
        distance = distance_arr[x].distance
        # are the points within an area of matching points
        if (area.contains(distance_arr[x].point_a) or area.touches(distance_arr[x].point_a)) and (
                area.contains(distance_arr[x].point_b) or area.touches(distance_arr[x].point_b)):
            count += 1
            if distance > maximum:
                maximum = distance
    print("end of kth")
    if count == 0:
        return -1
    return maximum


def hausdorff(point_set_a, point_set_b):
    distances_a = minimise_euclidean_normal(point_set_a, point_set_b)


    point_set = []
    # append all distances that are within 0.2 and append them
    for x in range(len(point_set_a)):
        if hasattr('abc','distance') == False:
            break
        if distances_a[x].distance < 0.2:
            point_set.append(distances_a[x].point_a)
    matching_points = MultiPoint(point_set)
    # use minimum rotated rectangle to outline the area of matching points
    area = matching_points.minimum_rotated_rectangle

    distances_b = minimise_euclidean_normal(point_set_b, point_set_a)
    multi = MultiPoint(point_set)

    # find the largest separate distance
    max_a = find_kth(distances_a, area)
    max_b = find_kth(distances_b, area)
    print("end of Hausdorff")
    if max_a > max_b:
        return max_a
    return max_b


def main():
    square = gs.square_set(2, 6)
    square2 = gs.diamond_set(0, 2)
    gs.display_data(square, square2)
    square2 = pm.translations(square2, 0.2, 0)
    print("Hausdorff distance: ", hausdorff(square, square2))


if __name__ == "__main__":
    main()
