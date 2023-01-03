from os import listdir, path
from parser import read_map_file, listFilesInDir
from genetic_Solver import create_graph,genetic_algorithm, fitness
from graphic_util import print_path
import time
import statistics


def generate_solution(graph, algorithm, scoreGetter):
    start_time = time.time()  
    solution = algorithm(graph, 2, 10, 10, 10)  
    end_time = time.time()  

    elapsed_time = end_time - start_time  
    
    score = scoreGetter(solution, graph)  
    
    return solution, score, elapsed_time  

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

    #number of times to run the algorithm
    num_runs = 10

    scores = []  
    elapsed_times = [] 
    for file in files[:2]:
        print("Currently on file : " + file)
        map_data = read_map_file(file)
        g1 = create_graph(map_data[0])

        for _ in range(num_runs):
            solution, score, elapsed_time = generate_solution(g1, genetic_algorithm, fitness)
            scores.append(score)
            elapsed_times.append(elapsed_time)
            solutions.append(solution)

    # average score for each instance
    average_scores = []
    for i in range(0, len(scores), num_runs):
        average_scores.append(sum(scores[i:i+num_runs]) / num_runs)

    # average time for each instance
    average_times = []
    for i in range(0, len(elapsed_times), num_runs):
        average_times.append(sum(elapsed_times[i:i+num_runs]) / num_runs)

    for i, file in enumerate(files):
        print("\n\n---------------------------------------------")
        print(f"Average score for {file}: {average_scores[i]:.3f}")
        print(f"Average time for {file}: {average_times[i]:.3f}")


