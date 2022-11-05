from descartes import PolygonPatch
from matplotlib import pyplot

import numpy as np
from matplotlib import pyplot as plt
from shapely.geometry import LineString, Polygon


#from figures import SIZE, set_limits, plot_coords, plot_bounds, plot_line_issimple


def display_data(multi, multi2):
    square_y = []
    square_x = []
    xs = [point.x for point in multi]
    ys = [point.y for point in multi]
    pointx = [0.25]
    pointy = [0.25]
    pointyy = [0.0]
    fig = pyplot.figure(1, dpi=90)

    # 1: valid multi-polygon
    #ax = fig.add_subplot(121)

    #patch = PolygonPatch(polygon, facecolor='blue', edgecolor='blue', alpha=0.5, zorder=2)
    #ax.add_patch(patch)
    if multi2 != 0:
        xs2 = [point.x for point in multi2]
        ys2 = [point.y for point in multi2]

        plt.scatter(xs2, ys2, s=20, color="green")
        plt.scatter(xs, ys, s=10, color="red")
        #plt.scatter(pointx, pointy,s=10, color='green')
        #plt.scatter(pointyy, pointy, s=10, color='black')
    else:

        plt.scatter(xs, ys, s=20, color="brown")
    with plt.style.context('dark_background'):
        #plt.gca().set_aspect('equal', adjustable='box')
        plt.axis('scaled')
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
    plt.axis('scaled')
    plt.show()

def display_final_data_pattern(multi, data):
    square_y = []
    square_x = []
    quincunx_x = []
    quincunx_y = []
    double_x = []
    double_y = []
    hexagon_x = []
    hexagon_y = []
    rectangle_x = []
    rectangle_y = []
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
            if point.shape == "quincunx":
                quincunx_x.append(point.point.x)
                quincunx_y.append(point.point.y)
            if point.shape == "double":
                double_x.append(point.point.x)
                double_y.append(point.point.y)
            if point.shape == "hexagon":
                hexagon_x.append(point.point.x)
                hexagon_y.append(point.point.y)
            if point.shape == "rectangle":
                rectangle_x.append(point.point.x)
                rectangle_y.append(point.point.y)
            if point.shape == "none":
                none_x.append(point.point.x)
                none_y.append(point.point.y)
    #plt.scatter(xs, ys, s=2, color='pink')
    plt.scatter(square_x, square_y, s=0.5, color='red')
    plt.scatter(quincunx_x, quincunx_y, s=0.5, color='blue')
    plt.scatter(hexagon_x, hexagon_y, s=0.5, color='green')
    plt.scatter(rectangle_x, rectangle_y, s=0.5, color='brown')
    plt.scatter(double_x, double_y, s=0.5, color='yellow')
    plt.scatter(none_x, none_y, s=0.5, color='black')
    plt.axis('scaled')
    with plt.style.context('dark_background'):
        plt.show()

COLOR = {
    True:  '#6699cc',
    False: '#ffcc33'
    }
def v_color(ob):
    return COLOR[ob.is_simple]

def plot_coords(ax, ob):
    x, y = ob.xy
    ax.plot(x, y, 'o', color='#999999', zorder=1)

def plot_bounds(ax, ob):
    x, y = zip(*list((p.x, p.y) for p in ob.boundary))
    ax.plot(x, y, 'o', color='#000000', zorder=1)

def plot_line(ax, ob):
    x, y = ob.xy
    ax.plot(x, y, color=v_color(ob), alpha=0.7, linewidth=3, solid_capstyle='round', zorder=2)

def plot_Line_String(line):
    fig = pyplot.figure(1,  dpi=90)
    ax = fig.add_subplot(121)


    plot_coords(ax, line)
    plot_bounds(ax, line)
    #plot_line_issimple(ax, line, alpha=0.7)

    ax.set_title('a) simple')

   # set_limits(ax, -1, 4, -1, 3)