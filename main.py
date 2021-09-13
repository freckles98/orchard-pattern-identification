
import generateShape as gs
import polygonManipulation as pm
from polygonManipulation import normalize_data
from polygonManipulation import best_pattern_match
import displayData as dd


def run_experiment():

    # Use a breakpoint in the code line below to debug your script.
    orchard_number = input("Please orchard enter number: ")
    window_size = input("Please enter window size: ")
    orchard_file = "raw_"+orchard_number+".geojson"
    ave = gs.determine_ave_confidence(orchard_file)
    print("Average: ", ave[0])
    print("Standard deviation: ", ave[1])

    data = gs.importData(orchard_file, ave[0] - ave[1])
    dd.display_data(data[0],0)
    data = normalize_data(data)

    best_match = best_pattern_match(data, int(window_size))
    #gs.display_data(best_match[2], window_size)
# Press the green button in the gutter to run the script.

def run_test():
    data = gs.square_set(0,0,20,15, True)
    window_size = 10
    best_match = best_pattern_match(data, int(window_size))

def test_2():
    data = gs.mixedShape()
    window_size = 5
    best_match = best_pattern_match(data, int(window_size))



if __name__ == '__main__':
    test_2()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
