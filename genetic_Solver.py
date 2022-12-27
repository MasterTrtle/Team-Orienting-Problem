# from the map to generate the graph
# each node is a position in the map where the score is not 0
# each edge is a path between two nodes
# the weight of the edge is the eucledian distance of the path
# we use NetworkX to create the graph

import random
import matplotlib.pyplot as plt
import networkx as nx

def get_score(graph, vehicule):
    # return the score of the path except the start and the end
    score = 0
    for node in vehicule:
        if graph.nodes[node]['score'] != "S" and graph.nodes[node]['score'] != "E":
            score += graph.nodes[node]['score']
    return score


def is_valid(agent, graph, max_distance):
    # check if the solution is valid
    # the solution is valid if the distance of each agent is less than the max_distance
    for vehicule in agent:
        if get_distance(graph, vehicule) > max_distance:
            return False
    return True

def get_distance(graph, vehicule):
    # return the distance of the agent

    distance = 0
    for i in range(len(vehicule) - 1):
        distance += graph[vehicule[i]][vehicule[i + 1]]['weight']
    return distance



def get_start_end(graph):
    # get the start and end nodes
    for node in graph.nodes:
        if graph.nodes[node]['score'] == "S":
            start = node
        elif graph.nodes[node]['score'] == "E":
            end = node
        elif graph.nodes[node]['score'] == "B":
            start = node
            end = node
    return start, end


def create_graph(map_data):
    # create a graph
    G = nx.Graph()
    # add nodes
    for i in range(len(map_data)):
        for j in range(len(map_data[0])):
            if map_data[i][j] != 0:
                G.add_node((i, j), score=map_data[i][j])

    # add edges for each node, the weight is the eucledian distance
    for node in G.nodes:
        for neighbor in G.nodes:
            if neighbor != node:
                G.add_edge(node, neighbor, weight=((node[0] - neighbor[0]) ** 2 + (node[1] - neighbor[1]) ** 2) ** 0.5)
    # draw the graph, position is the position of the nodes, the weight is the weight of the edges, the points are very far
    # away from each other, so the edges are not visible
    #nx.draw(G, pos=nx.spring_layout(G), with_labels=True, node_size=100, width=0.1)
    #plt.show()
    return G


def visitabled_path(graph, current_position, current_distance, start, end, max_distance):
    # return the list of nodes that can be visited from the current position
    visitabled = []
    not_visitabled = []
    # for each node in the graph apart from the current position, the end and the start
    for node in graph.nodes:
        if node != current_position and node != end and node != start:
            if graph[current_position][node]['weight'] + graph[node][end]['weight'] + current_distance <= max_distance:
                visitabled.append(node)
            else:
                not_visitabled.append(node)
    graph.remove_nodes_from(not_visitabled)

    return visitabled

# insert random nodes in the path
def insert_random_nodes(graph, agent, path, max_distance):
    visited = []
    for vehicule in agent:
        for node in vehicule:
            visited.append(node)
    # get the nodes that are not visited, except the start and the end
    not_visited = []
    for node in graph.nodes:
        if node not in visited and node != path[0] and node != path[-1]:
            not_visited.append(node)

    #suffle the path index except the start and the end
    path_index = list(range(1, len(path) - 1))
    random.shuffle(path_index)
    #suffle unvisited nodes
    random.shuffle(not_visited)
    #insert the nodes in the path
    current_distance = get_distance(graph, path)
    for i in path_index:
        for node in not_visited:
            if get_distance(graph, path[:i] + [node] + path[i:]) <= max_distance:
                path.insert(i, node)
                not_visited.remove(node)
                break

    return path







def generate_random_path(graph, start, end, max_distance):
    # while the agent can go further, go further
    modified_graph = graph.copy()
    path = [start]
    current_distance = 0
    current_position = start
    # weight of the edge between the start and end node
    # print(start, end, " distance = ",graph[start][end]['weight'])
    visitabled = visitabled_path(modified_graph, current_position, current_distance, start, end, max_distance)
    while visitabled != []:
        visitabled = visitabled_path(modified_graph, current_position, current_distance, start, end, max_distance)
        # choose a random node from the visitabled nodes
        new_position = random.choice(visitabled)
        path.append(new_position)
        current_distance += modified_graph[current_position][new_position]['weight']
        # delete the current_position from the graph if it is not the end or the start
        if current_position != start and current_position != end:
            modified_graph.remove_node(current_position)
        current_position = new_position
        visitabled = visitabled_path(modified_graph, current_position, current_distance, start, end, max_distance)
    # add the end to the path
    path.append(end)
    return path


def generate_random_solution(graph, start, end, nb_vehicule, max_distance):
    # generate a random solution for each agent
    # copy the graph
    modified_graph = graph.copy()
    solution = []
    for i in range(nb_vehicule):
        solution.append(generate_random_path(modified_graph, start, end, max_distance))
        # remove the nodes that are in the path of the agent except the start and the end
        for node in solution[i]:
            if node != start and node != end:
                modified_graph.remove_node(node)
    return solution


def generate_first_generation(graph, start, end, nb_vehicule, max_distance, nb_agent):
    # generate the first generation
    generation = []
    for i in range(nb_agent):
        generation.append(generate_random_solution(graph, start, end, nb_vehicule, max_distance))
    return generation


def fitness(agent, graph):
    # return the fitness of the solution
    # the fitness is the sum of the score of each vehicule
    fitness = 0
    for vehicule in agent:
        fitness += get_score(graph, vehicule)
    return fitness


def crossover(agent1, agent2, graph, max_distance):
    # This function takes in two parent solutions, parent1 and parent2,
    # as well as the input graph and the maximum allowed distance max_distance.
    # It then performs the crossover operation by selecting a random block of genes from parent1 and inserting it into a random position in parent2.
    # It then removes any repeated vertices in the resulting child solution and checks that the total distance does not exceed the maximum allowed distance. If the total distance does exceed the maximum allowed distance,
    # the function returns parent1, otherwise it returns the child solution.

    #select a random vehicule from the first agent
    vehicule1 = random.choice(agent1).copy()
    #select a random vehicule from the second agent, using index
    index = random.randint(0, len(agent1) - 1)
    vehicule2 = agent2[index].copy()

    # select a random block of genes from vehicule1, aprt from the start and the end
    block = random.sample(vehicule1[1:-1], random.randint(1, len(vehicule1) - 2)).copy()

    # select a random position in vehicule2 apart from the start and the end
    position = random.randint(1, len(vehicule2) - 2)

    # create the child first vehicule
    child = [vehicule2[:position].copy() + block.copy() + vehicule2[position:].copy()]

    #create the child other vehicules
    for vehicule in agent2:
        new_vehicule = []
        #if its index is not the same as the index of the vehicule selected
        if agent2.index(vehicule) != index:
            for node in vehicule[1:-1]:
                #if the node is not in the child1
                if node not in child:
                    #add it to the child
                    new_vehicule.append(node)
            #add the start and the end
            new_vehicule = [vehicule[0]] + new_vehicule.copy() + [vehicule[-1]]
            #add the vehicule to the child
            child.append(new_vehicule.copy())

    used_nodes = []
    #remove the repeated nodes
    for vehicule in child:
        for node in vehicule[1:-1]:
            if node not in used_nodes:
                used_nodes.append(node)
            else:
                vehicule.remove(node)
    #check if the child is valid
    if is_valid(child, graph, max_distance):
        #print("a child is born ! with a score of ", fitness(child, graph))
        return child.copy()
    else:
        return agent1

def mutation(agent, graph):
    # mutation of one vehicule of the agent
    # avalid solution can alter its own genetic code by
    # randomly modifying the genes order. In this case we
    # decided to perform a simple position switch by first
    # selecting one vertex (or gene) from one of the
    # agent and exchange with the vertex right after
    # that selected one, in the same list

    # copy the agent
    new_agent = agent.copy()

    # chose a copy of random vehicule using index
    index1 = random.randint(0, len(agent) - 1)
    vehicule = agent[index1].copy()

    index = random.randint(1, len(vehicule) - 3)
    # switch the two nodes
    vehicule[index], vehicule[index + 1] = vehicule[index + 1], vehicule[index]

    # if the new vehicule take a shorter path, replace the old one
    if get_distance(graph, vehicule) < get_distance(graph, agent[index1]):
        # print("the vehicule ", new_agent, " has been mutated")
        # print("mutation, we swape the nodes ", vehicule[index], " and ", vehicule[index + 1])
        new_agent[index1] = vehicule

    return new_agent


def mutation2(agent, graph):
    #copy the agent
    new_agent = agent.copy()
    #chose a random vehicule using index
    index1 = random.randint(0, len(agent) - 1)
    vehicule = new_agent[index1].copy()

    #chose a random node using index
    index = random.randint(1, len(vehicule) - 2)
    node = vehicule[index]
    #remove the node
    vehicule.remove(node)
    #chose a random position using index
    index = random.randint(1, len(vehicule) - 2)
    #insert the node in the new position
    vehicule.insert(index, node)
    #if the new vehicule take a shorter path, replace the old one
    if get_distance(graph, vehicule) < get_distance(graph, agent[index1]):
        #print("the vehicule ", new_agent, " has been mutated")
        #print("mutation, we swape the nodes ", vehicule[index], " and ", vehicule[index + 1])
        new_agent[index1] = vehicule

    return new_agent

def mutation3(agent, graph, max_distance):
    #get all visited nodes
    visited = []
    for vehicule in agent:
        for node in vehicule[1:-1]:
            visited.append(node)

    #copy the agent
    new_agent = agent.copy()
    #chose a random vehicule using index
    index1 = random.randint(0, len(agent) - 1)
    vehicule = new_agent[index1].copy()

    #chose a random node using index
    index = random.randint(1, len(vehicule) - 2)
    node = vehicule[index]
    #remove the node
    vehicule.remove(node)

    #insert random nodes in the vehicule until the distance is too long
    vehicule = insert_random_nodes(graph, agent, vehicule, max_distance)

    #if the new agent is fitter, replace the old one
    if get_score(graph, vehicule) > get_score(graph, agent[index1]):
        #print("the vehicule ", new_agent, " has been mutated")
        new_agent[index1] = vehicule

    return new_agent




def genetic_algorithm(graph, nb_vehicule, max_distance, nb_agent = 30, nb_generation = 100):
    start, end = get_start_end(graph)

    # generate the first generation
    generation = generate_first_generation(graph, start, end, nb_vehicule, max_distance, nb_agent)

    for i in range(nb_generation):
        # select the 20% best solutions of the current generation
        best_agent = []

        # calculate the fitness of each agent
        fitness_generation = [fitness(agent, graph) for agent in generation]
        new_generation = []

        # get first 10 max fitness values index
        from heapq import nlargest
        max_fitness_index = nlargest(10, range(len(fitness_generation)), fitness_generation.__getitem__)
        # get the best agents
        for index in max_fitness_index:
            best_agent.append(generation[index].copy())

        # add the best agents to the new generation
        for agent in best_agent:
            new_generation += [agent.copy()]

        # mutation each of the best agent 5 times
        for agent in best_agent:
            for k in range(5):
                new_generation.append(mutation(agent, graph))
                new_generation.append(mutation2(agent, graph))
                new_generation.append(mutation3(agent, graph, max_distance))

                # print(get_distance(graph, mutant[0]) - get_distance(graph, agent[0]))

        # crossover each of the best agent with each other

        for agent1 in best_agent:
            for agent2 in best_agent:
                if agent1 != agent2:
                    child = crossover(agent1, agent2, graph, max_distance).copy()
                    new_generation.append(child)

        #generate random agents
        for i in range(10):
            new_generation.append(generate_first_generation(graph, start, end, nb_vehicule, max_distance, 1)[0])

        generation = new_generation.copy()
        #print("generation ", i+1, " : ", max(fitness_generation))

    # for i, agent in enumerate(generation):
    #     print("_________________________________________________________")
    #     print("agent number ", i, " : ")
    #     print(sum([get_distance(graph, vehicule) for vehicule in agent]))
    #     print("score = ", fitness(agent, graph))

    #select agent with the best fitness
    fitness_generation = [fitness(agent, graph) for agent in generation]
    best_agent_index = fitness_generation.index(max(fitness_generation))
    best_agent = generation[best_agent_index]
    #select among the best agent the one with the lowest distance
    best_agent = sorted(best_agent, key=lambda vehicule: get_distance(graph, vehicule))
    print("the best agent is : ", best_agent, " with a score of ", fitness(best_agent, graph))

    return best_agent