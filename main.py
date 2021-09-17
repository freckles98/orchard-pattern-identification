
import generateShape as gs
import polygonManipulation as pm
from polygonManipulation import normalize_data
from polygonManipulation import best_pattern_match
import displayData as dd
import hausdorffDistance as hd


def run_experiment():

    # Use a breakpoint in the code line below to debug your script.
    orchard_number = input("Please orchard enter number: ")
    window_size = input("Please enter window size: ")
    orchard_file = "raw_"+orchard_number+".geojson"
    ave = gs.determine_ave_confidence(orchard_file)
    print("Average: ", ave[0])
    print("Standard deviation: ", ave[1])

    data = gs.import_data(orchard_file, ave[0] - ave[1])
    #dd.display_data(data[0],0)
    data = normalize_data(data)
    #dd.display_data(data, 0)

    best_match = best_pattern_match(data, int(window_size), False)
    #gs.display_data(best_match[2], window_size)
# Press the green button in the gutter to run the script.

def run_test():
    data = gs.square_set(0,0,20,15, True)
    window_size = 10
    best_match = best_pattern_match(data, int(window_size), False)

def test_2():
    data = gs.mixed_shape()
    window_size = 10
    best_match = best_pattern_match(data, int(window_size), False)
def drawing():
    data = gs.rectangle_set(0,0,8,8,True)

    dd.display_data(data,0)

def testtt():
    a = (1,2)
    b = (1,7)
    angle = pm.angle_between(b,a)
    print(angle)
def test_3():
    data = gs.multiple_mixed_pattern()
    dd.display_data(data,0)
    best_match = best_pattern_match(data, int(6), False)
def test_4():
    data = gs.square_set(0,0,5,5,True)
    model = gs.double_row(0,5,True)
    hd.partial_hausdorff(model, data)
if __name__ == '__main__':
    test_4()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
