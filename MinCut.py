
def min_cut(graph, node)
    A = [node]
    nodes = graph.get_nodeset()
    V = nodes
    V_update = list(set(V)-set(A))
    while A != V
        for n in V_update
            edges = n.get_incident_edges



