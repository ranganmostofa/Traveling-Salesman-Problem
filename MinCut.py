
def min_cut(graph, node):
    A = node
    nodes = graph.get_nodeset()
    V = nodes
    while A != V:
        V_update = list(set(V.difference(set(A))))
        adj_nodes = node.get_incident_edges()







        for n in A:
            edges = n.get_incident_edges()
            for edge in edges:
                other_node = {node for node in edge.get_incident_nodes() if not node.get_name().__eq__()}.pop()
                other_node.get_incident_edges()




