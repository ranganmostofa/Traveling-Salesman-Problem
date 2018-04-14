from time import time
from DataIO import DataIO
from StoerWagner import StoerWagner
from UndirectedGraph import UndirectedGraph


t_0 = time()

filename = "synthetic8.txt"

dict_graph = DataIO.read_graph("./../Data/" + filename)

G = UndirectedGraph.dictionary_to_undirected_graph_form(dict_graph)

minimum_cut, minimum_cut_weight = StoerWagner.apply(G, G.get_node_names().pop())

t_1 = time()

print "\nMinimum Cut: " + str(minimum_cut) + "\n"
print "Minimum Cut Weight: " + str(minimum_cut_weight) + "\n"

print "Time Taken: " + str(t_1 - t_0) + "s\n"

