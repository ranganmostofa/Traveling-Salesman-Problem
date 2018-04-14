#from gurobipy import *
from time import time
from DataIO import DataIO
from StoerWagner import StoerWagner
from UndirectedGraph import UndirectedGraph

filename = r"C:\Users\marco_000\Traveling-Salesman-Problem_new\Data\synthetic8.txt"

weights = {}
with open(filename, 'r') as file:
    num_nodes, num_edges = DataIO._preprocess_line(file.readline())
    for line in file.readlines():
        preprocessed_line = DataIO._preprocess_line(line)
        if preprocessed_line:
            source_node, terminal_node, weight = preprocessed_line
            weights[source_node, terminal_node] = weight
            weights[terminal_node, source_node] = weight

print(weights)
print(filename)
# Create Model
m = Model("TSP")

# Create variables
variables = {}
for i in range(num_nodes):
    for j in range(i+1):
        variables[i, j] = m.addVar(obj= weighy[i, j], vtype=GRB.BINARY, name='e'+str(i)+'_'+str(j))
        variables[j, i] = variables[i, j]
#m.update()