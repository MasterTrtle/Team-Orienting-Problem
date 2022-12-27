import tkinter as tk
import random
from genetic_Solver import get_start_end

def print_path(graph, agent):
    # print a board with the path of the agent, using tkinter
    # create the window
    root = tk.Tk()
    root.title("Path")
    root.geometry("800x800")
    # create the canvas
    canvas = tk.Canvas(root, width=800, height=800)
    canvas.pack()


    for i in range(0, 800, 50):
        tk.Canvas(root, width=800, height=2, bg="black").place(x=0, y=i)
        tk.Canvas(root, width=2, height=800, bg="black").place(x=i, y=0)


    # color the start and the end
    start, end = get_start_end(graph)
    tk.Canvas(root, width=50, height=50, bg="green").place(x=start[0] * 50, y=start[1] * 50)
    tk.Canvas(root, width=50, height=50, bg="red").place(x=end[0] * 50, y=end[1] * 50)

    # print the nodes score on the board, at
    for node in graph:
        if node != start and node != end:
            # center the text
            x = node[0] * 50 + 25
            y = node[1] * 50 + 25
            # print the text
            tk.Label(root, text=str(graph.nodes[node]['score']), font=("Arial", 10)).place(x=x, y=y)

    # draw arrow between the nodes of the agent using canvas, change the color for each vehicule
    for vehicule in agent:
        color = random.choice(["red", "blue", "green", "yellow", "orange", "purple", "pink", "brown", "grey", "black"])
        for i in range(len(vehicule) - 1):
            node1 = vehicule[i]
            node2 = vehicule[i + 1]
            # get the coordinates of the nodes
            x1 = node1[0] * 50 + 25
            y1 = node1[1] * 50 + 25
            x2 = node2[0] * 50 + 25
            y2 = node2[1] * 50 + 25
            # draw the arrow

            tk.Canvas(root, width=2, height=2, bg=color).place(x=x1, y=y1)
            tk.Canvas(root, width=2, height=2, bg=color).place(x=x2, y=y2)
            canvas.pack()

            canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, fill=color)

    root.mainloop()