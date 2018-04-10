from gurobipy import *
from time import time
from DataIO import DataIO
from StoerWagner import StoerWagner
from UndirectedGraph import UndirectedGraph

filename = "synthetic8.txt"

with open(filename, 'r') as file:
    num_nodes, num_edges = DataIO.__preprocess_line(file.readline())

# Create Model
m = Model("TSP")

# Create Variables
i = 1
for node in num_nodes:
    node = m.addVar(vtype=GRB.BINARY, name=("x"+str(i)))
    i += 1


