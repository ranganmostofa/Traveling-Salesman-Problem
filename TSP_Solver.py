from time import time
from gurobipy import *
from DataIO import DataIO
from StoerWagner import StoerWagner
from UndirectedGraph import UndirectedGraph


t0 = time()

graph_filename = "hk48.txt"

relative_path = "./Data/" + graph_filename

weights = DataIO.read_graph(relative_path)

num_nodes = len(weights)

# Create Model
model = Model("TSP")

# Create variables
variables = {}
for i in range(num_nodes):
    for j in weights[i].keys():
        if j in weights[i]:
            if not (j, i) in variables:
                variable = model.addVar(obj=weights[i][j], vtype=GRB.BINARY, name='e' + str(i) + '_' + str(j))
                variables[tuple((i, j))] = variable

# Add Degree-2 Constraints
for i in weights.keys():
    lhs = LinExpr()
    for pair, var in variables.items():
        if i in pair:
            lhs.add(var)
    model.addConstr(lhs == 2)

iter_index = 1

while True:

    print "\nIteration Number: " + str(iter_index) + "\n"

    model.update()
    model.optimize()

    # print "\n"
    # for pair, var in variables.items():
    #     print str(pair) + ": " + str(var.X)

    duplicate_weights = DataIO.read_graph(relative_path)
    for pair, var in variables.items():
        i, j = pair
        duplicate_weights[i][j] = var.X
        duplicate_weights[j][i] = var.X

    graph = UndirectedGraph.dictionary_to_undirected_graph_form(duplicate_weights)
    minimum_cut, minimum_cut_weight = StoerWagner.apply(graph, graph.get_node_names().pop())

    partitionA, partitionB = minimum_cut
    sec_lhs = LinExpr()
    for i in partitionA:
        for j in partitionB:
            if tuple((int(i), int(j))) in variables.keys():
                sec_lhs.add(variables[tuple((int(i), int(j)))])
            elif tuple((int(j), int(i))) in variables.keys():
                sec_lhs.add(variables[tuple((int(j), int(i)))])
    model.addConstr(sec_lhs >= 2)

    iter_index += 1

    if minimum_cut_weight >= 2:
        break

t1 = time()

model.write("hk48_out5.lp")

# DataIO.write_tour(weights, model, graph_filename.split(".").pop(0) + "_tour.txt")


print "Total time taken: " + str(t1 - t0) + " seconds"

