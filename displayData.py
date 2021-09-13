import numpy as np
from matplotlib import pyplot as plt


def display_data(multi, multi2):
    square_y = []
    square_x = []
    xs = [point.x for point in multi]
    ys = [point.y for point in multi]


    if multi2 != 0:
        xs2 = [point.x for point in multi2]
        ys2 = [point.y for point in multi2]

        plt.scatter(xs2, ys2, s=20, color="blue")
        plt.scatter(xs, ys, s=10, color="orange")
    else:

        plt.scatter(xs, ys, s=1)
    with plt.style.context('dark_background'):
        plt.show()

def display_data_pattern(multi, data):
    square_y = []
    square_x = []
    diamond_x = []
    diamond_y = []
    double_x = []
    double_y = []
    xs = [point.x for point in data]
    ys = [point.y for point in data]

    for list in multi:
        for point in list:
            print(point.point.x, point.point.y, point.confidence, point.shape)
            if point.shape == "none":
                if point.confidence < 0.22:
                    square_x.append(point.point.x)
                    square_y.append(point.point.y)

            if point.shape == "quincunx":
                diamond_x.append(point.point.x)
                diamond_y.append(point.point.y)
            if point.shape == "double":
                double_x.append(point.point.x)
                double_y.append(point.point.y)
    plt.scatter(xs, ys, s=0.5, color='blue')
    plt.scatter(square_x, square_y, s=1, color='red')
    plt.scatter(diamond_x, diamond_y, s=0.5, color='blue')
    plt.scatter(double_x, double_y, s=0.5, color='yellow')

    plt.show()

def display_final_data_pattern(multi, data):
    square_y = []
    square_x = []
    diamond_x = []
    diamond_y = []
    double_x = []
    double_y = []
    none_x = []
    none_y = []
    xs = [point.x for point in data]
    ys = [point.y for point in data]


    for point in multi:
        print(point.point.x, point.point.y, point.confidence, point.shape)
        if point.confidence == np.inf:
            none_x.append(point.point.x)
            none_y.append(point.point.y)
        else:
            if point.shape == "square":
                square_x.append(point.point.x)
                square_y.append(point.point.y)
            if point.shape == "quicunx":
                diamond_x.append(point.point.x)
                diamond_y.append(point.point.y)
            if point.shape == "double":
                double_x.append(point.point.x)
                double_y.append(point.point.y)
            if point.shape == "none":
                none_x.append(point.point.x)
                none_y.append(point.point.y)
    plt.scatter(xs, ys, s=0.5, color='blue')
    plt.scatter(square_x, square_y, s=1, color='red')
    plt.scatter(diamond_x, diamond_y, s=0.5, color='blue')
    plt.scatter(double_x, double_y, s=0.5, color='yellow')
    plt.scatter(none_x, none_y, s=0.5, color='black')
    with plt.style.context('dark_background'):
        plt.show()