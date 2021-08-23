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


def matching_the_pattern(model, data):
    print("ello")
    area = data.minimum_rotated_rectangle
    x, y = area.exterior.coords.xy
    print(x, y)
    print(55)
    max_x = max(x)
    max_y = max(y)
    print(0)
    model = translations(model, min(x), min(y))
    print(1)
    minimum = np.inf
    matching_model = [sys.maxsize, 0]

    switch = False
    flag = False
    print(2)
    # need to change the range
    for y in range(int(5)):
        for x in range(int(5)):
            print("HII")
            dist = hd.hausdorff(model, data)
            print("damn hello")
            if 0 <= dist < minimum:
                minimum = dist
            if dist != 0:
                if dist < matching_model[0]:
                    matching_model[0] = dist
                    matching_model[1] = model

                if switch == False:
                    model = translations(model, 0.2, 0)
                else:
                    model = translations(model, -0.2, 0)


            else:
                print("Hallelujah!", model)
                flag = True
                matching_model[0] = 0
                matching_model[1] = model
                break

        if switch:
            switch = False
        else:
            switch = True
        if flag == True:
            break
        model = translations(model, 0, 0.2)
        print("end of Y,", y)
    print("end of X", x)
    #gs.display_data(model, data)
    print("finished!")

    return minimum

def normalize_data():
    return


def main():
    model = gs.square_set(0, 20)
    print("Model Set")
    data1 = gs.diamond_set(10, 15)
    gs.display_data(data1,0)
    data2 = gs.square_set(10,15)
    data3 = gs.diamond_set(20,25)
    a = np.concatenate([data1, data2])
    data = np.concatenate([a, data3])
    #data = gs.to_multipoint(data)
    gs.display_data(data, 0)
    print("Data set")
    print(matching_the_pattern(model, data))


if __name__ == "__main__":
    main()