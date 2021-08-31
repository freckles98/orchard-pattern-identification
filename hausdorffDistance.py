import math

import numpy as np
from shapely.geometry import MultiPoint, Point, Polygon
from shapely.ops import nearest_points
from scipy.spatial import distance, cKDTree, KDTree
from sklearn.neighbors import BallTree


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


def nearest_neighbor(left_gdf, right_gdf, return_dist=False):
    left_radians = np.array(left_gdf.apply(lambda geom: (geom.x * np.pi / 180, geom.y * np.pi / 180)).to_list())
    right_radians = np.array(right_gdf.apply(lambda geom: (geom.x * np.pi / 180, geom.y * np.pi / 180)).to_list())
    closest, dist = get_nearest(src_points=left_radians, candidates=right_radians)
    # closest_points = right.loc[closest]
    print(closest, dist)


def ckdnearest(point, point_set_A):

    btree = cKDTree(point_set_A)
    dist, idx = btree.query(point, k=1)
    return (idx, dist)


def get_nearest(src_points, candidates, k_neighbors=1):
    """Find nearest neighbors for all source points from a set of candidate points"""

    # Create tree from the candidate points
    tree = BallTree(candidates, leaf_size=15, metric='haversine')

    # Find closest points and distances
    distances, indices = tree.query(src_points, k=k_neighbors)

    # Transpose to get distances and indices into arrays
    #distances = distances.transpose()
    #indices = indices.transpose()

    # Get closest indices and distances (i.e. array at index 0)
    # note: for the second closest points, you would take index 1, etc.
    closest = indices[0]
    closest_dist = distances[0]

    # Return indices and distances
    return (closest, closest_dist)


def minimise_euclidean_normal(point_set_a, point_set_b):
    distances_set = []
    counter = 0
    print("hello")
    list_arrays_B = [np.array((point.xy[0][0], point.xy[1][0])) for point in point_set_b]
    for point in point_set_a:
        newPoint = [np.array((point.xy[0][0], point.xy[1][0]))]

        # nearest_geoms = nearest_points(point, point_set_b)
        # print("Shapely method")
        # print(nearest_geoms[1])
        # dist = math.sqrt(((point.x - nearest_geoms[1].x) ** 2) + ((point.y - nearest_geoms[1].y) ** 2))
        # print(dist)
        nearest_geomss = ckdnearest(newPoint, list_arrays_B)
        distances_set.append(distances(point, point_set_b[nearest_geomss[0][0]], nearest_geomss[1][0]))
        counter += 1
    print("goodbye")
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
    print("Okay working")
    distances_a = minimise_euclidean_normal(point_set_a, point_set_b)
    print("done work")
    point_set = []
    # append all distances that are within 0.2 and append them
    for x in distances_a:
        if x.distance < 0.22:
            point_set.append(x.point_a)
    matching_points = MultiPoint(point_set)
    # use minimum rotated rectangle to outline the area of matching points
    area = matching_points.minimum_rotated_rectangle
    print("More work")
    distances_b = minimise_euclidean_normal(point_set_b, point_set_a)

    # find the largest separate
    print("maximums")
    max_a = find_kth(distances_a, area)
    max_b = find_kth(distances_b, area)
    print("maximums done")

    if max_a > max_b:
        return max_a
    return max_b


def main():
    print("begin")
    square = gs.square_set(0, 0, 120, 120, True)
    print("square done")
    square2 = gs.diamond_set(0, 0, 120, 120, True)
    # gs.display_data(square, square2)
    #    square2 = pm.translations(square2, 0.5, 0)
    print("Hausdorff distance: ", hausdorff(square, square2))



if __name__ == "__main__":
    main()
