from time import time
from gurobipy import *
from DataIO import DataIO
from StoerWagner import StoerWagner
from GraphVisualizer import GraphVisualizer
from UndirectedGraph import UndirectedGraph


def minimum_spanning_tree(graph):
    """

    :param graph:
    :return:
    """
    mst = []
    weight = 0
    mst.append(0)
    while len(mst) != len(graph):
        min2 = float('inf')
        node_add = 0
        new_w = 0
        for j in mst:
            inner_dict = graph[j]
            for k in inner_dict:
                if inner_dict[k] < min2 and k not in mst:
                    min2 = inner_dict[k]
                    new_w = min2
                    node_add = k
        mst.append(node_add)
        weight += new_w
    return mst, weight


t0 = time()

path = raw_input("Please enter path to file containing graph: ")

graph_filename = str(path).split("/").pop(0)

graph_prefix = str(graph_filename).split(".").pop()

weights = DataIO.read_graph(path)

num_nodes = len(weights.keys())

# Create Model
model = Model("TSP")

obj = LinExpr()

# Create variables
variables = {}
for i in range(num_nodes):
    for j in weights[i].keys():
        if j in weights[i]:
            if not (j, i) in variables:
                variable = model.addVar(obj=weights[i][j], vtype=GRB.BINARY, name=str(i) + '_' + str(j))
                obj.add(variable, weights[i][j])
                variables[tuple((i, j))] = variable

# Add Degree-2 Constraints
for i in weights.keys():
    lhs = LinExpr()
    for pair, var in variables.items():
        if i in pair:
            lhs.add(var)
    model.addConstr(lhs == 2)

mst, mst_weight = minimum_spanning_tree(weights)

model.addConstr(obj <= 2 * mst_weight)  # upper bound

iter_index = 1

while True:

    print "\nIteration Number: " + str(iter_index) + "\n"

    model.update()
    model.optimize()

    duplicate_weights = DataIO.read_graph(path)
    for pair, var in variables.items():
        i, j = pair
        duplicate_weights[i][j] = var.X
        duplicate_weights[j][i] = var.X

    graph = UndirectedGraph.dictionary_to_undirected_graph_form(duplicate_weights)
    minimum_cut, minimum_cut_weight = StoerWagner.apply(graph, graph.get_node_names().pop())

    if minimum_cut_weight >= 2:
        break

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


t1 = time()

model.write(graph_prefix + "_out.lp")

model.write(graph_prefix + "_out.sol")

DataIO.write_tour(weights, model, graph_prefix + "_tour.txt")

print "Total time taken: " + str(t1 - t0) + " seconds"

GraphVisualizer.disp_graph(weights)

