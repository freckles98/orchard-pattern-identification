from shapely.affinity import affine_transform, translate, rotate
import sys
import generateShape as gs
import hausdorffDistance as hd
import numpy as np


def rotations(point_set):
    return rotate(point_set, 1, origin='center')


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
    print(x, y)
    #model = translations(model, min(x), min(y))
    model = translations(model, 11, 0)
    gs.display_data(model, data)
    minimum = np.inf
    matching_model = MatchingModel(minimum, model)

    switch = False
    flag = False
    print(2)
    # need to change the range
    for y in range(int(5)):
        for x in range(int(5)):
            print("begin")
            dist = hd.hausdorff(model, data)
            print("Distance", dist)
            print("end")
            if 0 <= dist < minimum:
                minimum = dist
            if dist != 0:
                if dist < matching_model.distance:
                    matching_model = MatchingModel(dist, model)

                if switch == False:
                    model = translations(model, 0.2, 0)
                else:
                    model = translations(model, -0.2, 0)


            else:
                print("Hallelujah!", model)
                flag = True
                return MatchingModel(0, model)
            gs.display_data(model, data)

        if switch:
            switch = False
        else:
            switch = True
        if flag == True:
            break
        model = translations(model, 0, 0.2)

    if minimum == np.inf:
        print("no match")
    return matching_model

def normalize_data():
    return

def determine_data(data):
    model1 = gs.square_set(0, 0, 5, 5, True)
    model2 = gs.diamond_set(0, 0, 5, 5, True)
    model3 = gs.double_row(0, 5, True)
    min1 = matching_the_pattern(model1, data)
    min2 = matching_the_pattern(model2, data)
    min3 = matching_the_pattern(model3, data)
    print("Min1",min1.distance, "min2", min2.distance, "min3", min3.distance)

    if min1.distance == -1:
        if min2.distance == -1:
            if min3.distance == -1:
                print("No match")
            else:
                gs.display_data(min3.model, data)
                print("Matching pattern: double row")
        elif min3.distance == -1 or min2.distance < min3.distance:

            gs.display_data(min2.model, data)
            print("Matching pattern: diamond")

        else:
            gs.display_data(min3.model, data)
            print("Matching pattern: double row")
    elif min2.distance!= -1:
        if min3.distance != -1:
            if min1.distance < min2.distance and min1.distance < min3.distance:
                gs.display_data(min1.model, data)
                print("Matching pattern: square")
            elif min2.distance < min3.distance and min2.distance < min1.distance:
                gs.display_data(min2.model, data)
                print("Matching pattern: diamond")
            elif min3.distance < min1.distance and min3.distance < min2.distance:
                gs.display_data(min3.model, data)
                print("Matching pattern: double row")
        else:
            if min1.distance < min2.distance:
                gs.display_data(min1.model, data)
                print("Matching pattern: square")
            else:
                gs.display_data(min2.model, data)
                print("Matching pattern: diamond")
    else:
        gs.display_data(min1.model, data)
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


def main():


    data = gs.mixedShape()
    data = translations(data, 0.6, 0)
    gs.display_data(data, 0)
    determine_data(data)


if __name__ == "__main__":
    main()