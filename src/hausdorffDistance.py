import math

import numpy as np
from shapely.geometry import MultiPoint
from scipy.spatial import cKDTree

from src import generateShape as gs


class distances:
    def __init__(self, point_a, point_b, distance, index):
        self.point_a = point_a
        self.point_b = point_b
        self.distance = distance
        self.index = index

    def toStrings(self):
        print(self.point_a, self.point_b, self.distance)

def ckdnearest(point, btree):
    dist, idx = btree.query(point, k=1)
    return (idx, dist)


def minimise_euclidean_normal(point_set_a, point_set_b, cal_match):
    distances_set = []
    matching_set = []
    btree = cKDTree(point_set_b, balanced_tree=False)

    for index, point in enumerate(point_set_a):

        nearest_geoms = ckdnearest(point, btree)
        distances_set.append(distances(point, point_set_b[nearest_geoms[0]], nearest_geoms[1], index))
        #print("This is the nearest point", point.x, point_set_b[nearest_geoms[0]].x, point.y, point_set_b[nearest_geoms[0]].y)
        if cal_match and nearest_geoms[1] < 0.7:
            matching_set.append(point)
    return distances_set, matching_set


def find_maximum(distance_arr, area):
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
    print(count)
    if count == 0:
        return np.inf
    return maximum

def minimise_euclidean_normals(point_set_a, point_set_b):
    distances_set = []
    matching_set = []
    btree = cKDTree(point_set_b, balanced_tree=False)

    for index, point in enumerate(point_set_a):
        nearest_geoms = ckdnearest(point, btree)
        distances_set.append(distances(point, point_set_b[nearest_geoms[0]], nearest_geoms[1], index))

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
    print(count)
    if count == 0:
        return np.inf
    return maximum

def find_kth_ranked(distance_arr, area, f1=0.2):
    q = len(distance_arr)
    K = math.floor(f1*q)
    maximum = []

    for x in range(0, q, K):
        max = 0
        for point in distance_arr[x: x+K]:

            if (area.contains(point.point_a) or area.touches(point.point_a)) and (
                    area.contains(point.point_b) or area.touches(point.point_b)):
                if point.distance > max:
                    max = point.distance
        maximum.append(max)
    return min(maximum)



def find_average(distance_arr, area):
    maximum = 0
    count = 0
    ave = 0
    for x in distance_arr:
        distance = x.distance
        if (area.contains(x.point_a) or area.touches(x.point_a)) and (
                area.contains(x.point_b) or area.touches(x.point_b)):

            ave += distance
            count += 1
    if count == 0:
        return np.inf
    return ave/count

def adapted_partial_convex_hull(model, data):
    distances_a = minimise_euclidean_normal(model, data, True)
    distances_b = minimise_euclidean_normal(data, model, False)
    matching_points = MultiPoint(distances_a[1])
    area = matching_points.convex_hull
    max_a = find_kth(distances_a[0], area)
    max_b = find_kth(distances_b[0], area)
    return max(max_a, max_b)

def partial_hausdorff(model, data):
    area = data.convex_hull
    distances_a = minimise_euclidean_normals(model, data)
    distances_b = minimise_euclidean_normals(data, model)
    max_a = find_kth_ranked(distances_a, area)
    max_b = find_kth_ranked(distances_b, area)
    return max(max_a, max_b)

def average_hausdorff(model, data):
    area = data.convex_hull
    distances_a = hausdorff_ave(model, data, area)
    distances_b = hausdorff_ave(data, model, area)


    return max(distances_a, distances_b)

def hausdorff(model, data):
    area = data.convex_hull
    max_a = minimise_euclidean(model, data, area)
    max_b = minimise_euclidean(data, model, area)
    # use minimum rotated rectangle to outline the area of matching points

    # find the largest separate


    return max(max_a, max_b)

def minimise_euclidean(point_set_a, point_set_b, area):
    distances_set = []
    matching_set = []
    btree = cKDTree(point_set_b, balanced_tree=False)
    count = 0
    maximum = 0
    for index, point in enumerate(point_set_a):
        nearest_geoms = ckdnearest(point, btree)
        if (area.contains(point) or area.touches(point)) :
            count += 1

            if nearest_geoms[1] > maximum:
                maximum = nearest_geoms[1]
            if maximum > 1:
                return 1

    if count == 0:
        return np.inf
    return maximum

def hausdorff_ave(point_set_a, point_set_b, area):

    btree = cKDTree(point_set_b, balanced_tree=False)
    count = 0
    ave = 0
    for index, point in enumerate(point_set_a):
        nearest_geoms = ckdnearest(point, btree)
        if (area.contains(point) or area.touches(point)) :
            count += 1
            ave += nearest_geoms[1]

    if count == 0:
        return np.inf
    return ave/count




def main():
    print("begin")
    square = gs.square_set(0, 0, 61, 61, True)
    print("square done")
    square2 = gs.diamond_set(0, 0, 10, 10, True)
    # gs.display_data(square, square2)
    #    square2 = pm.translations(square2, 0.5, 0)
    print("Hausdorff distance: ", hausdorff(square, square2))


if __name__ == "__main__":
    main()
