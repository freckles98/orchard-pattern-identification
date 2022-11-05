import math
import random

import shapely.affinity
from shapely.affinity import translate, rotate, scale
from shapely.geometry import Point, Polygon

from src import generateShape as gs, displayData as dd, hausdorffDistance as hd
import numpy as np


class PatternNode:
    def __init__(self, point, shape, confidence):
        self.point = point
        self.shape = shape
        self.confidence = confidence


class MatchingModel:
    def __init__(self, distance, model):
        self.distance = distance
        self.model = model


def rotations(point_set):
    return rotate(point_set, 15, origin='center')


def rotate_back(point_set):
    return rotate(point_set, -180, origin='center')


def translations(point_set, x, y):
    return translate(point_set, x, y, 0)


def normalize_data(data):
    num_trees = data[1]
    centroids = data[0]
    print(num_trees)

    convex = centroids.convex_hull
    area = convex.area
    print(area)
    density = num_trees / area

    centroids = shapely.affinity.scale(centroids, math.sqrt(density), math.sqrt(density))
    centroids = scale(centroids, 0.55, 0.55) #cheeky scaling
    rectangle = centroids.minimum_rotated_rectangle
    x, y = rectangle.exterior.coords.xy
    translation_index = y.index(min(y))
    translation_x = x[translation_index]  # x
    translation_y = y[translation_index]  # y

    rotation_index = x.index(max(x))
    rotation_x = x[rotation_index]  # a
    rotation_y = y[rotation_index]  # b
    distance_x = math.sqrt((translation_x - rotation_x) ** 2 + (translation_y - translation_y) ** 2)
    distance_y = math.sqrt((rotation_x - rotation_x) ** 2 + (rotation_y - translation_y) ** 2)
    angle = math.atan(distance_y / distance_x)
    centroids = rotate(centroids, -angle, origin=Point(translation_x, translation_y), use_radians=True)
    centroids = translations(centroids, -translation_x, -translation_y)

    return centroids



def rotation_approximation(model, data_set,data_arr):
    def takePoint(elem):
        return elem.x

    sorted_list = sorted(data_arr, key = lambda x:x.x)
    dd.display_data(sorted_list[0:15],0)
    sorted_by_y = sorted(sorted_list[0:15], key = lambda y:y.y)
    dd.display_data(sorted_by_y[0:15], 0)
    dict = {1: [0], 2: [0], 3: [0], 4: [0]}
    for x in range(len(data_set)-1):
        random_num = random.randint(0, len(data_set) - 2)
        # print(random_num)

        point1 = data_set[x]
        point2 = data_set[x + 1]

        hypotenuse = point1.distance(point2)
        point3 = Point(point2.x, point1.y)
        adjacent = point2.distance(point3)
        angle = math.acos(adjacent / hypotenuse) * 180 / math.pi
        # print("This is the angle ",angle, point1, point2, point3)

        if point1.y > point2.y:
            if point1.x > point2.x:
                # Quadrant 1
                arr = dict.get(1)
                arr[0] = arr[0] + 1
                arr.append(angle)
                dict[1] = arr


            elif point1.x == point2.x:
                pass
            else:
                arr = dict.get(2)
                arr[0] = arr[0] + 1
                arr.append(angle)
                dict[2] = arr
                # Quadrant 2
        else:
            if point1.x > point2.x:
                arr = dict.get(4)
                arr[0] = arr[0] + 1
                arr.append(angle)
                dict[4] = arr

            elif point1.x == point2.x:
                pass
            else:
                arr = dict.get(3)
                arr[0] = arr[0] + 1
                arr.append(angle)
                dict[3] = arr

    max = [0, 0]
    for x in range(1, 5):
        count = dict.get(x)[0]

        if max[1] < count:
            max[0] = x
            max[1] = count


    common_arr = dict.get(max[0])
    if max[0] > 2:
        opposite_arr = dict.get(max[0]-2)
    else:
        opposite_arr = dict.get(max[0] + 2)

    accum = 0
    for x in range(1, len(common_arr)):
        accum += common_arr[x]
    for y in range(1, len(opposite_arr)):
        accum += opposite_arr[y]

    average = accum / (len(common_arr)+len(opposite_arr) - 2)

    rotated_model = model
    if max[0] == 1 or max[0] == 3:
        rotated_model = rotate(model, average, origin='center')
    if max[0] == 2 or max[0] == 3:
        rotated_model = rotate(model, -average, origin='center')
    return rotated_model


def matching_the_pattern(model, data_set, shape, implement_rotations, data_arr):
    minimum = np.inf
    matching_model = MatchingModel(minimum, model)
    final_pattern = []
    rotation_range = 0
    switch = False
    flag = False
    rotated_model = model
    #rotated_model = rotation_approximation(model, data_set, data_arr)
    if shape == "rectangle":
        increments = 10
    else:
        increments = 5

    for y in range(increments):
        for x in range(increments):
            if implement_rotations:
                if shape == "square" or shape == "quincunx":
                    rotation_range = 6
                elif shape == "double" or shape == "rectangle":
                    rotation_range = 12
                else:
                    rotation_range = 24
                rotated_model = model
                for z in range(rotation_range):

                    dist = hd.average_hausdorff(rotated_model, data_set)

                    if 0 <= dist < matching_model.distance:
                        matching_model = MatchingModel(dist, rotated_model)
                    rotated_model = rotations(model)
                rotated_model = model

            if not implement_rotations:

                dist = hd.average_hausdorff(rotated_model, data_set)


                if 0 <= dist < matching_model.distance:
                    matching_model = MatchingModel(dist, rotated_model)

            if x+1 < increments:
                if switch == False:
                    model = translations(model, 0.2, 0)
                else:
                    model = translations(model, -0.2, 0)

        if switch:
            switch = False
        else:
            switch = True
        if flag == True:
            break
        model = translations(model, 0, 0.2)

    # print(matching_model.distance)
    final_pattern = assign_pattern(matching_model.distance, shape, data_set)
    # gs.display_data(matching_model.model, data_set)
    return (matching_model, final_pattern)


def assign_pattern(minimum, shape, data):
    pattern = []
    for point in data:
        pattern.append(PatternNode(point, shape, minimum))
    return pattern

def angle_between(p1, p2):
    ang1 = np.arctan2(*p1[::-1])
    ang2 = np.arctan2(*p2[::-1])
    return np.rad2deg((ang1 - ang2) % (2 * np.pi))



def execute_over_entire_pattern(model, data, shape, data_set_range, window_size, implement_rotations):
    area = data.minimum_rotated_rectangle
    xcord, ycord = area.exterior.coords.xy

    list_of_matches = []
    switch = False
    pattern = []
    for y in range(0, int(max(ycord)), window_size):


        for x in range(0, int(max(xcord)), window_size):

            data_set = []
            for point in data:
                if data_set_range.contains(point) or data_set_range.touches(point):
                    data_set.append(point)
            multi_data_set = gs.to_multipoint(data_set)


            # print(line_data_set)
            # print(multi_data_set)
            #dd.display_data(line_data_set,0)
            # change this not hausdorff best pattern match
            if len(multi_data_set) > 0:
                matches = matching_the_pattern(model, multi_data_set, shape, implement_rotations, data_set)
                pattern.append(matches[1])

                list_of_matches.append(matches[0])
                dd.display_data(matches[0].model,multi_data_set)
                #print(matches[0].distance)
                #dd.display_data(data_set,0)
            if x + window_size < int(max(xcord)):
                if not switch:
                    model = translations(model, window_size, 0)
                    data_set_range = translations(data_set_range, window_size, 0)
                else:
                    model = translations(model, -window_size, 0)
                    data_set_range = translations(data_set_range, -window_size, 0)

        if switch:
            switch = False
        else:
            switch = True

        model = translations(model, 0, window_size)
        data_set_range = translations(data_set_range, 0, window_size)
        print("Okay going up", y)

    return list_of_matches, pattern

def find_maximum(square, hexagon, quincunx, double, rectangle):
    arr = [square, hexagon,quincunx,double, rectangle]
    min_val = np.inf
    min_idx = 6
    for inx, num in enumerate(arr):
        if min_val == num.confidence:
            print("THE SAME, THE SAME")

        if min_val > num.confidence:
            min_val = num.confidence
            min_idx = inx

    if min_val == np.inf:
        return PatternNode(arr[0].point, "none", np.inf)
    return PatternNode(arr[min_idx].point, arr[min_idx].shape, arr[min_idx].confidence)


def best_pattern_match(data, window_size, implement_rotations):
    data_set_range = Polygon([(0, 0), (window_size , 0), (window_size, window_size ), (0, window_size )  ])

    model1 = gs.square_set(-1, -1, window_size + 3, window_size + 3, True)
    model2 = gs.quincunx_set(-1, -1, window_size + 3, window_size + 3, True)
    model3 = gs.double_row(-1, window_size + 3, True)
    model4 = gs.hexagonal_set(-1, window_size + 3, True)
    model5 = gs.rectangle_set(-1, -1, window_size + 3, window_size + 3, True)

    min1 = execute_over_entire_pattern(model1, data, "square", data_set_range, window_size, implement_rotations)
    pattern_square = min1[1]

    min2 = execute_over_entire_pattern(model2, data, "quincunx", data_set_range, window_size, implement_rotations)
    pattern_quincunx = min2[1]
    min3 = execute_over_entire_pattern(model3, data, "double", data_set_range, window_size, implement_rotations)
    pattern_double_row = min3[1]

    min4 = execute_over_entire_pattern(model4, data, "hexagon", data_set_range, window_size, implement_rotations)
    pattern_hexagon = min4[1]

    min5 = execute_over_entire_pattern(model5, data, "rectangle", data_set_range, window_size, implement_rotations)
    pattern_rectangle = min5[1]
    pattern = []

    for index, list in enumerate(pattern_square):

        for point in range(len(list)):


            pattern.append(find_maximum(pattern_square[index][point],pattern_hexagon[index][point],
                                        pattern_quincunx[index][point], pattern_double_row[index][point], pattern_rectangle[index][point]))


    dd.display_final_data_pattern(pattern, data)
    return pattern


def initialize_pattern_node(points):
    pattern = []
    for index, point in enumerate(points):
        pattern.append(PatternNode(Point(point.x, point.y), "none", np.inf))
    return pattern


def main():
    orchard_number = input("Please orchard enter number: ")
    window_size = input("Please enter window size: ")
    orchard_file = "raw_" + orchard_number + ".geojson"
    ave = gs.determine_ave_confidence(orchard_file)
    print("Average: ", ave[0])
    print("Standard deviation: ", ave[1])

    data = gs.import_data(orchard_file, ave[0] - ave[1])
    data = normalize_data(data)
    dd.display_data(data,0)

    best_match = best_pattern_match(data, int(window_size), True)
    dd.display_data(best_match[2], window_size)


if __name__ == "__main__":
    main()
