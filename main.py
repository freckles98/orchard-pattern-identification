# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import generateShape as gs
import polygonManipulation as pm


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
    square = gs.square_set(0,0,10,10,True)
    gs.display_data(square, 0)
    square = pm.rotations(square)
    gs.display_data(square, 0)
    square = pm.rotations(square)
    gs.display_data(square, 0)
    square = pm.rotations(square)
    gs.display_data(square, 0)
    square = pm.rotations(square)
    gs.display_data(square, 0)
    square = pm.rotations(square)
    gs.display_data(square, 0)
    square = pm.rotations(square)
    gs.display_data(square, 0)

    diamond = gs.diamond_set(0,0,10,10,True)
    gs.display_data(diamond,0)
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
