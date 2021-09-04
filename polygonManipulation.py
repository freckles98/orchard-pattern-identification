import math

import shapely.affinity
from shapely import affinity
from shapely.affinity import affine_transform, translate, rotate
import sys

from shapely.geometry import Point

import generateShape as gs
import hausdorffDistance as hd
import numpy as np


class PatternNode:
    def __init__(self, xcoord, ycoord, shape, confidence):
        self.xcoord = xcoord
        self.ycoord = ycoord
        self.shape = shape
        self.confidence = confidence


def rotations(point_set):
    return rotate(point_set, 15, origin='center')


def translations(point_set, x, y):
    return translate(point_set, x, y, 0)


def hausdorff_distance(model, data):
    return data.hausdorff_distance(model)


def partial_hausdorff_distance():
    return


class MatchingModel:
    def __init__(self, distance, model):
        self.distance = distance
        self.model = model


def matching_the_pattern(model, data):
    area = data.minimum_rotated_rectangle
    x, y = area.exterior.coords.xy
    #print(x, y)
    # model = translations(model, min(x), min(y))
    #print("pre transition", model)
    #model = translations(model, 9, 0)
    #print("post transition", model)
    #gs.display_data(model, data)
    minimum = np.inf
    matching_model = MatchingModel(minimum, model)

    switch = False
    flag = False

    # need to change the range
    for y in range(int(5)):
        for x in range(int(5)):
            dist = hd.hausdorff(model, data)
            if 0 <= dist < minimum:
                minimum = dist
            if dist != 0:
                if 0 < dist < matching_model.distance:
                    matching_model = MatchingModel(dist, model)

                if switch == False:
                    model = translations(model, 0.2, 0)
                else:
                    model = translations(model, -0.2, 0)


            else:
                #print("Hallelujah!", model)
                flag = True
                return MatchingModel(0, model)

        if switch:
            switch = False
        else:
            switch = True
        if flag == True:
            break
        model = translations(model, 0, 0.2)
        gs.display_data(model, data)

    #if minimum == np.inf:
        #print("no match")
    return matching_model


def normalize_data(data):
    num_trees = data[1]
    centroids = data[0]
    convex = centroids.convex_hull
    area = convex.area
    density = num_trees / area
    print(math.sqrt(density))
    centroids = shapely.affinity.scale(centroids, math.sqrt(density), math.sqrt(density))
    rectangle = centroids.minimum_rotated_rectangle
    x, y = rectangle.exterior.coords.xy
    translation_index = y.index(min(y))
    translation_x = x[translation_index] #x
    translation_y = y[translation_index] #y

    rotation_index = x.index(max(x))
    rotation_x = x[rotation_index] #a
    rotation_y = y[rotation_index] #b
    distance_x = math.sqrt((translation_x - rotation_x)**2+(translation_y - translation_y)**2)
    distance_y = math.sqrt((rotation_x - rotation_x)**2+(rotation_y - translation_y)**2)
    angle = math.atan(distance_y/distance_x)
    centroids = rotate(centroids, -angle, origin=Point(translation_x, translation_y),use_radians=True)
    gs.display_data(centroids, 0)
    centroids = translations(centroids, -translation_x,-translation_y)




    gs.display_data(centroids, 0)
    return centroids


def best_pattern_match(data):
    model1 = gs.square_set(0, 0, 30, 30, True)
    model1 = rotations(model1)
    model2 = gs.diamond_set(0, 0, 30, 30, True)
    model3 = gs.double_row(0, 30, True)
    gs.display_data(model1,0)
    min1 = execute_over_entire_pattern(model1, data)
    min2 = execute_over_entire_pattern(model2, data)
    min3 = execute_over_entire_pattern(model3, data)
    print("Min1", min1[0].distance, "min2", min2[0].distance, "min3", min3[0].distance)
    for x in range(len(min1)):
        if min1[x].distance == -1:
            if min2[x].distance == -1:
                if min3[x].distance == -1:
                    print("No match")
                else:
                    # gs.display_data(min3[x].model, data)
                    print("Matching pattern: double row")
                    return min3[x].model, "Double"
            elif min3[x].distance == -1 or min2[x].distance < min3[x].distance:

                # gs.display_data(min2[x].model, data)
                print("Matching pattern: diamond")
                return min2[x].model, "Diamond"

            else:
                # gs.display_data(min3[x].model, data)
                print("Matching pattern: double row")
        elif min2[x].distance != -1:
            if min3[x].distance != -1:
                if min1[x].distance < min2[x].distance and min1[x].distance < min3[x].distance:
                    # gs.display_data(min1[x].model, data)
                    print("Matching pattern: square")
                    return min1[x].model, "Square"
                elif min2[x].distance < min3[x].distance and min2[x].distance < min1[x].distance:
                    # gs.display_data(min2[x].model, data)
                    print("Matching pattern: diamond")
                elif min3[x].distance < min1[x].distance and min3[x].distance < min2[x].distance:
                    # gs.display_data(min3[x].model, data)
                    print("Matching pattern: double row")
            else:
                if min1[x].distance < min2[x].distance:
                    # gs.display_data(min1.model, data)
                    print("Matching pattern: square")
                    return min1[x].model, "Square"
                else:
                    # gs.display_data(min2[x].model, data)
                    print("Matching pattern: diamond")
        else:
            # gs.display_data(min1[x].model, data)
            print("Matching pattern: square")

    # if 0 < min1.distance < min2.distance and 0 < min1.distance < min3.distance:
    #     gs.display_data(min1.model, data)
    #     print("Matching pattern: square")
    # elif 0 < min2.distance < min3.distance and 0 < min2.distance < min1.distance:
    #     gs.display_data(min2.model, data)
    #     print("Matching pattern: diamond")
    # elif 0 < min3.distance < min1.distance and 0 < min3.distance < min2.distance:
    #     gs.display_data(min3.model, data)
    #     print("Matching pattern: double row")
    # else:
    #     print("error")


def execute_over_entire_pattern(model, data):
    area = data.minimum_rotated_rectangle
    xcord, ycord = area.exterior.coords.xy
    #print(xcord, ycord)
    count = 0
    list_of_matches = []
    switch = False
    #print("Xcord", xcord, "Ycord", ycord)
    for y in range(int(max(ycord)/10)):
        for x in range(int(max(xcord)/10)):

            # change this not hausdorff best pattern match

            list_of_matches.append(matching_the_pattern(model, data))

            count += 1

            if not switch:
                model = translations(model, 10, 0)
            else:
                model = translations(model, -10, 0)

        if switch:
            switch = False
        else:
            switch = True
        model = translations(model, 0, 10)
        print("Okay going up", y)
        gs.display_data(model, data)
    return list_of_matches


def main():
    print("let the games begin")
    data = gs.importData()
    data = normalize_data(data)
    #data = translations(data, 0.5, 0)
    #data = affinity.scale(data, xfact=1.2, yfact=1.2)
    #gs.display_data(data[0], 0)
   # print(data2)
    print(best_pattern_match(data))


if __name__ == "__main__":
    main()
