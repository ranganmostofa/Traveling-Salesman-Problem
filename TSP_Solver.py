from gurobipy import *
from time import time
from DataIO import DataIO
from StoerWagner import StoerWagner
from UndirectedGraph import UndirectedGraph

filename = r"C:\Users\marco_000\Traveling-Salesman-Problem_new\Data\synthetic8.txt"

weights = DataIO.read_graph(filename)
print(weights)
# Create Model
m = Model("TSP")

# Create variables
variables = {}
for i in range(num_nodes):
    for j in range(i+1):
        variables[i, j] = m.addVar(obj= weights[i, j], vtype=GRB.BINARY, name='e'+str(i)+'_'+str(j))
        variables[j, i] = variables[i, j]
#m.update()