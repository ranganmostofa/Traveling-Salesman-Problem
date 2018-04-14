#from gurobipy import *
from time import time
from DataIO import DataIO
from StoerWagner import StoerWagner
from UndirectedGraph import UndirectedGraph

filename = "synthetic8.txt"

weight = {}
with open(filename, 'r') as file:
    num_nodes, num_edges = DataIO.__preprocess_line(file.readline())
    for line in file.readlines():
        preprocessed_line = DataIO.__preprocess_line(line)
        if preprocessed_line:
            source_node, terminal_node, weight = preprocessed_line
            weight[source_node, terminal_node] = weight
            weight[terminal_node, source_node] = weight

print(weight)
print(filename)
# Create Model
m = Model("TSP")

# Create variables
variables = {}
for i in range(num_nodes):
    for j in range(i+1):
        variables[i, j] = m.addVar(obj= ##############, vtype=GRB.BINARY, name='e'+str(i)+'_'+str(j))
        #vars[j, i] = vars[i, j]
#m.update()