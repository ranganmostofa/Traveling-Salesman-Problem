from gurobipy import *
from time import time
from DataIO import DataIO
from StoerWagner import StoerWagner
from UndirectedGraph import UndirectedGraph


# filename = r"C:\Users\marco_000\Traveling-Salesman-Problem_new\Data\synthetic8.txt"  # for Marco
filename = "./Data/synthetic8.txt"  # for Rangan

weights = DataIO.read_graph(filename)

num_nodes = len(weights)

# Create Model
m = Model("E4T 4$$")

# Create variables
variables = {}
for i in range(num_nodes):
    for j in weights[i].keys():
        if j in weights[i]:
            if not (j, i) in variables:
                variable = m.addVar(obj=weights[i][j], vtype=GRB.BINARY, name='e'+str(i)+'_'+str(j))
                variables[tuple((i, j))] = variable

# Add Degree-2 Constraints
for i in weights.keys():
    lhs = LinExpr()
    for pair, var in variables.items():
        if i in pair:
            lhs.add(var)
    m.addConstr(lhs == 2)

m.update()
# print(variables)
m.optimize()

for pair, var in variables.items():
    print str(pair) + ": " + str(var.X)

