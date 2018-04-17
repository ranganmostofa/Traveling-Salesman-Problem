from time import time
from gurobipy import *
from DataIO import DataIO
from StoerWagner import StoerWagner
from GraphVisualizer import GraphVisualizer
from UndirectedGraph import UndirectedGraph


def minimum_spanning_tree(graph):
    """
    Given a graph represented as a dictionary, computes and returns the minimum spanning tree of
    the input graph
    """
    mst = []  # initialize a list to record the edges
    weight = 0  # initialize the total weight to zero
    mst.append(0)  # add 0 to the ordering of vertices
    while len(mst) != len(graph):  # while all vertices have not been added yet
        min2 = float('inf')  # initialize to negative infinity
        node_add = 0
        new_w = 0
        for j in mst:  # for every node in the graph
            inner_dict = graph[j]  # retrieve the inner dictionary
            for k in inner_dict:  # for every node in the inner dictionary
                if inner_dict[k] < min2 and k not in mst:  # get the minimum edge
                    min2 = inner_dict[k]
                    new_w = min2
                    node_add = k
        mst.append(node_add)  # append the next node
        weight += new_w  # add the weight to the tally
    return mst, weight  # return the final ordering and the total weight


def construct_tour(graph, tsp_model):
    """
    Given a graph represented as a dictionary and a gurobi model object, constructs the optimal tour
    solved by the model as a dictionary and returns the tour
    """
    tour = {}  # initialize the tour
    for node in graph.keys():  # for every node in the graph
        tour[node] = {}  # add the node
    for decision_variable in tsp_model.getVars():  # for every binary decision variable in the model
        if decision_variable.getAttr("X"):  # if the value is set to one
            variable_name = decision_variable.getAttr("VarName")  # get the variable name
            i, j = (int(num) for num in variable_name.split("_"))  # retrieve the node names
            if j in graph[i].keys():  # check for internal ordering
                tour[i][j] = graph[i][j]  # and store the weight
            else:
                tour[i][j] = graph[j][i]
    return tour  # return the final tour


t0 = time()  # start recording

path = raw_input("Please enter path to file containing graph: ")  # prompt for path to file

graph_filename = str(path).split("/").pop()  # retrieve the filename

graph_prefix = str(graph_filename).split(".").pop(0)  # retrieve the graph name

weights = DataIO.read_graph(path)  # read the graph

num_nodes = len(weights.keys())  # get the number of nodes in the graph

GraphVisualizer.disp_graph(weights, graph_prefix + "_graph")  # visualize the original graph

# Create Model
model = Model("TSP")

obj = LinExpr()  # linear expression object for the objective function

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

mst, mst_weight = minimum_spanning_tree(weights)  # compute the mst weight

model.addConstr(obj <= 2 * mst_weight)  # upper bound of 2 * MST weight

iter_index = 1  # initialize iteration index

while True:  # enter infinite loop - see below for termination criterion

    print "\nIteration Count: " + str(iter_index) + "\n"  # print the iteration count

    model.update()  # update the model

    model.optimize()  # solve the program

    duplicate_weights = DataIO.read_graph(path)  # duplicate the graph
    for pair, var in variables.items():  # superimpose the binary decision variable values on the edge weights
        i, j = pair
        duplicate_weights[i][j] = var.X
        duplicate_weights[j][i] = var.X

    graph = UndirectedGraph.dictionary_to_undirected_graph_form(duplicate_weights)  # create graph object

    # get minimum cut and corresponding weight
    minimum_cut, minimum_cut_weight = StoerWagner.apply(graph, graph.get_node_names().pop())

    if minimum_cut_weight >= 2:  # if the minimum cut weight is greater than or equal to 2
        break  # break from infinite loop
    else:  # otherwise
        tour = construct_tour(weights, model)  # construct current tour
        GraphVisualizer.disp_graph(tour, graph_prefix + "_tour_" + str(iter_index))  # display the graph
        while raw_input("\nHit enter to proceed to next iteration: "): pass  # ask for input to proceed
        print "\n"

    partitionA, partitionB = minimum_cut  # add subtour-elimination constraints to the model based on the minimum cut
    sec_lhs = LinExpr()
    for i in partitionA:
        for j in partitionB:
            if tuple((int(i), int(j))) in variables.keys():
                sec_lhs.add(variables[tuple((int(i), int(j)))])
            elif tuple((int(j), int(i))) in variables.keys():
                sec_lhs.add(variables[tuple((int(j), int(i)))])
    model.addConstr(sec_lhs >= 2)

    iter_index += 1  # update the iteration counter

t1 = time()  # stop recording the time

model.write(graph_prefix + "_out.lp")  # output the lp file using gurobi

model.write(graph_prefix + "_out.sol")  # output the sol file using gurobi

# output the optimal tour according to the project specifications
DataIO.write_tour(weights, model, graph_prefix + "_tour.txt")

print "Total time taken: " + str(t1 - t0) + " seconds"  # print the total time taken to solve

optimal_tour = construct_tour(weights, model)  # construct the optimal tour

GraphVisualizer.disp_graph(optimal_tour, graph_prefix + "_optimal_tour")  # visualize the optimal tour

