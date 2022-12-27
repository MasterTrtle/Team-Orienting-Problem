from os import listdir, path

ignoreList = [".ipynb", "README", ".nis", ".blb", ".ris"]

def shouldIgnoreFile(fileName):
    for i in ignoreList:
        if i in fileName:
            return True
    
    return False



def listFilesInDir(dirs):
    listFiles = []
    for dir in dirs:
        for f in listdir(dir):
            if path.isfile(dir+'/'+f) and not shouldIgnoreFile(f):
                listFiles.append(dir+'/'+f)
            elif path.isdir(dir+'/'+f):
                listFiles += listFilesInDir([dir+'/'+f])
    
    return listFiles


def read_map_file(file_path):
    # Open the file and read the contents
    with open(file_path, 'r') as f:
        lines = f.readlines()

        # Extract the metadata from the first three lines
        # num_vertices = n
        # num_paths = m
        # max_time_per_path = tmax

        num_vertices = int(lines[0].split()[1])
        num_paths = int(lines[1].split()[1])
        max_time_per_path = int(float(lines[2].split()[1]))
    # Create a list to store the map data
    map_data = []

    # Read the data for each point
    for line in lines[3:]:
        # Split the line on the tab character
        x, y, s = line.strip().split('\t')
        # Add the data to the map_data
        map_data.append([int(float(x)), int(float(y)), int(float(s))])

    # create map, a list of list, where map[i][j] = score, else 0
    # map is a rectangle, lenght = max x, width = max y
    map = [[0 for i in range(max([x[1] for x in map_data]) + 1)] for j in range(max([x[0] for x in map_data]) + 1)]

    for i in map_data[1:-1]:
        map[i[0]][i[1]] = i[2]

    if map_data[0][0] == map_data[-1][0] and map_data[0][1] == map_data[-1][1]:
        #if starting and ending point are the same
        map[map_data[0][0]][map_data[0][1]] = "B"
    else:
        # the starting point is the first point in the map_data
        map[map_data[0][0]][map_data[0][1]] = "S"

        # the ending point is the last point in the map_data
        map[map_data[-1][0]][map_data[-1][1]] = "E"

    # Return the map data
    return map, num_vertices, num_paths, max_time_per_path
