from os import listdir, path
from parser import read_map_file, listFilesInDir
from genetic_Solver import create_graph,genetic_algorithm, fitness
from graphic_util import print_path
import time
import statistics
import csv
import pandas as pd
import random
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import networkx as nx
from matplotlib.lines import Line2D




def generate_solution(graph, algorithm, scoreGetter):
    start_time = time.time()

    while(True):
        error = False
        #try:
        solution = algorithm(graph, 2, 10, 30, 80)  
        #except Error as e:
        #    print("except")
         #   error = True
        if not error:
            break

    
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

    #print(files)

    #number of times to run the algorithm
    num_runs = 3

    scores = []  
    elapsed_times = [] 

    random.shuffle(files)
    filesCopy = files.copy()
    print(len(files))
    for file in filesCopy[1:1]:
        print("Currently on file : " + file)
        
        try:
            map_data = read_map_file(file)
            g1 = create_graph(map_data[0])

            for _ in range(num_runs):
                solution, score, elapsed_time = generate_solution(g1, genetic_algorithm, fitness)
                scores.append(score)
                gs.append(g1)
                elapsed_times.append(elapsed_time)
                solutions.append(solution)
        except:
            files.remove(file)



    # average score for each instance
    average_scores = []
    for i in range(0, len(scores), num_runs):
        average_scores.append(sum(scores[i:i+num_runs]) / num_runs)

    # average time for each instance
    average_times = []
    for i in range(0, len(elapsed_times), num_runs):
        average_times.append(sum(elapsed_times[i:i+num_runs]) / num_runs)

    lResults = []
    for i in range(len(average_scores)):
        lResults.append([files[i], average_scores[i], average_times[i], solutions[i], gs[i].nodes, gs[i].edges])
        print("\n\n---------------------------------------------")
        print(f"Average score for {files[i]}: {average_scores[i]:.3f}")
        print(f"Average time for {files[i]}: {average_times[i]:.3f}")

  #  with open('results.csv', mode='w') as csv_file:
 #       fieldnames = ['file', 'average_score', 'average_time', 'solution', 'nodes', 'edges']
#        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        #writer.writeheader()
        #for i in range(len(average_scores)):
        #    writer.writerow({'file': files[i], 'average_score': average_scores[i], 'average_time': average_times[i], 'solution': solutions[i], 'nodes': len(gs[i].nodes), 'edges': len(gs[i].edges)})

    # load the data from the CSV file
    data = pd.read_csv('results.csv')
    x=data.average_score
    y=data.average_time
    plt.scatter(data.average_score, data.average_time)
    plt.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))
         (np.unique(x)), color='red')   
    plt.title("Average score - average time") 
    plt.show()
    sns.regplot(x='average_score', y='average_time', data=data)
    plt.title("Average score - average time") 
    plt.show()
    sns.regplot(x='nodes', y='average_time', data=data)
    plt.title("Average Time - Nodes") 
    plt.xlabel("Number of Nodes")
    plt.ylabel("Average Time")
    plt.show()
    sns.regplot(x='nodes', y='average_score', data=data)
    plt.title("Average Score - Nodes") 
    plt.xlabel("Number of Nodes")
    plt.ylabel("Average Score")
    plt.show()
    sns.regplot(x='edges', y='average_time', data=data)
    plt.title("Average time - edges") 
    plt.xlabel("Number of edges")
    plt.ylabel("Average time")
    plt.show()


    sns.regplot(x='edges', y='average_score', data=data)
    plt.title("Average Score - Edges") 
    plt.xlabel("Number of Edges")
    plt.ylabel("Average Score")
    plt.show()
    sns.regplot(x='nodes', y='edges', data=data)
    plt.title("Nodes - Edges") 
    plt.xlabel("Number of Nodes")
    plt.ylabel("Number of Edges")
    plt.show()
    sns.lmplot(x='nodes', y='average_time', hue='edges', data=data)
    plt.title("Average Time - Nodes/Edges") 
    plt.xlabel("Number of Nodes")
    plt.ylabel("Average Time")
    plt.show()
    # analyze the data
    print(data.describe())
