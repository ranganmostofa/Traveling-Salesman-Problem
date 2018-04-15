from GraphProcessing import GraphProcessing


class NearestNeighborAlgorithm:
    """

    """
    @staticmethod
    def apply(G, root_name):
        """

        :param G:
        :param root_name:
        :return:
        """
        if root_name not in G.get_node_names():
            raise Exception("Error: The input root node is not contained in the input graph")
        induced_ordering = list([root_name])
        next_vertex = GraphProcessing.search_node_names(G.get_nodeset(), root_name)
        while len(induced_ordering) != len(G.get_node_names()):
            next_vertex = NearestNeighborAlgorithm.determine_nearest_neighbor(next_vertex, induced_ordering)
            induced_ordering.append(next_vertex.get_name())
        return induced_ordering

    @staticmethod
    def determine_nearest_neighbor(current_vertex, induced_ordering):
        """

        :param current_vertex:
        :param induced_ordering:
        :return:
        """
        weight_map = \
            dict({
                edge: edge.get_weight()
                for edge in current_vertex.get_incident_edges()
                if edge.get_other_node(current_vertex.get_name()).get_name() not in induced_ordering
            })

        optimum_edge = max(weight_map, key=weight_map.get)

        return optimum_edge.get_other_node(current_vertex.get_name())

