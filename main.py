from os import listdir, path
from parser import read_map_file, listFilesInDir
from genetic_Solver import create_graph,genetic_algorithm
from graphic_util import print_path

if __name__ == '__main__':
    # for each instance in each set folder in the Instances folder apart from

    # instances = []
    # for set_folder in listdir('Instances'):
    #     for instance in listdir('Instances/' + set_folder):
    #         # read the map file
    #         map_data = read_map_file('Instances/' + set_folder + '/' + instance)
    #         instances += [map_data]   
    startingDirectories = ["Instances"]
    files = []

    gs = []
    solutions = []

    print("Listing files")
    files = listFilesInDir(startingDirectories)

    print(files)


    for file in files:
        print("Currently on file : " + file)
        #map_data = read_map_file('Instances/Set_21_234/p2.2.b.txt')
        map_data = read_map_file(file)
        g1 = create_graph(map_data[0])


        
        solution = genetic_algorithm(g1, 2, 10)
        print_path(g1, solution)

        gs.append(g1)
        solutions.append(solution)
