from time import time
from DataIO import DataIO
from StoerWagner import StoerWagner
from UndirectedGraph import UndirectedGraph


t_0 = time()

graph_filename = "att48.txt"

relative_path = "./Data/" + graph_filename

dict_graph = DataIO.read_graph(relative_path)

G = UndirectedGraph.dictionary_to_undirected_graph_form(dict_graph)


def minimum_spanning_tree(dict1):
    mst = []
    weight = 0
    mst.append(0)
    while len(mst) != len(dict1):
        min2 = float('inf')
        node_add = 0
        new_w = 0
        for j in mst:
            inner_dict = dict1[j]
            for k in inner_dict:
                if inner_dict[k] < min2 and k not in mst:
                    min2 = inner_dict[k]
                    new_w = min2
                    node_add = k
        mst.append(node_add)
        weight += new_w
    return mst, weight

m, w = minimum_spanning_tree(dict_graph)
# minimum_cut, minimum_cut_weight = StoerWagner.apply(G, G.get_node_names().pop())

t_1 = time()

print(m)
print(w)
print(str(t_1 - t_0))

# print "\nMinimum Cut: " + str(minimum_cut) + "\n"
# print "Minimum Cut Weight: " + str(minimum_cut_weight) + "\n"

# print "Time Taken: " + str(t_1 - t_0) + "s\n"

