from gurobipy import *
from time import time
from DataIO import DataIO
from StoerWagner import StoerWagner
from UndirectedGraph import UndirectedGraph

filename = r"C:\Users\marco_000\Traveling-Salesman-Problem_new\Data\synthetic8.txt"

weights = DataIO.read_graph(filename)
print(weights)
num_nodes = len(weights)
# Create Model
m = Model("TSP")
# Create variables
variables = []
for i in range(num_nodes):
    for j in weights[i].keys():
        if j in weights[i]:
            if not (j, i) in variables:
                m.addVar(obj=weights[i][j], vtype=GRB.BINARY, name='e'+str(i)+'_'+str(j))
                variables.append((i, j))
m.update()
print(variables)