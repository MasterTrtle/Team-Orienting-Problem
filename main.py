from os import listdir
from parser import read_map_file

if __name__ == '__main__':
    # for each instance in each set folder in the Instances folder apart from
    instances = []
    for set_folder in listdir('Instances'):
        for instance in listdir('Instances/' + set_folder):
            # read the map file
            map_data = read_map_file('Instances/' + set_folder + '/' + instance)
            instances += [map_data]
