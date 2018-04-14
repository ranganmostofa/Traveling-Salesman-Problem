from GraphProcessing import GraphProcessing


class StoerWagner:
    """
    Class that houses Python implementation of the global minimum cut algorithm on undirected
    weighted graphs lacking a source and terminal node, as presented by Stoer & Wagner in
    their 1997 paper, "A Simple Min Cut Algorithm".

    Link to paper: https://fktpm.ru/file/204-stoer-wagner-a-simple-min-cut-algorithm.pdf
    """

    CONNECTION_STRENGTH_ATTRIBUTE = "connection strength"  # attribute key for connection strength

    MERGED_NODE_NAME_DELIMITER = ","  # delimiter for merged node names

    @staticmethod
    def apply(G, initial_node_name):
        """
        Given an UndirectedGraph object and the initial node name, applies the Stoer-Wagner algorithm to
        compute the minimum cut of the graph
        """
        minimum_cut = tuple()  # initialize the minimum cut and its corresponding weight
        minimum_cut_weight = float('inf')  # initialized to a very large positive number
        G_prime = G.__deepcopy__()  # construct a deepcopy of the input graph
        while len(G_prime.get_nodeset()) > 1:  # while the cardinality of the vertex set is greater than one
            # perform a single iteration of the minimum cut phase
            G_prime, current_cut = StoerWagner.__minimum_cut_phase(G_prime, initial_node_name)
            # evaluate the weight of the current cut
            current_cut_weight = StoerWagner.evaluate_cut_weight(G, current_cut)
            if current_cut_weight < minimum_cut_weight:  # if the weight is lower than the stored weight
                minimum_cut = current_cut  # store the current cut and its weight as the stored cut and weight
                minimum_cut_weight = current_cut_weight
        return tuple(minimum_cut), float(minimum_cut_weight)  # return the minimum cut and its corresponding weight

    @staticmethod
    def __minimum_cut_phase(G, initial_node_name):
        """
        Given an UndirectedGraph object and the initial node name, performs a single minimum cut phase
        iteration and returns the resulting contracted graph and the current cut of the phase
        """
        # initialize the induced ordering, connections strengths and the next vertex to be added to the induced ordering
        induced_ordering = list([initial_node_name])
        G_prime = StoerWagner.__initialize_connection_strengths(G)
        next_vertex = GraphProcessing.search_node_names(G_prime.get_nodeset(), initial_node_name).pop()
        while set(induced_ordering) != G_prime.get_node_names():  # while not all vertices have been ordered
            # determine the next vertex in the ordering
            next_vertex = StoerWagner.__determine_most_tightly_connected_vertex(G_prime, induced_ordering, next_vertex)
            induced_ordering.append(next_vertex.get_name())  # add the vertex to the ordering
        # construct the set of vertices to be merged
        merge_nodelist = StoerWagner.__get_merge_nodelist(induced_ordering)
        current_cut = StoerWagner.__construct_current_cut(induced_ordering)  # construct the cut partitions
        G_prime.contract_graph(
            merge_nodelist,
            StoerWagner.MERGED_NODE_NAME_DELIMITER.join(merge_nodelist)
        )  # perform graph contraction based on the list of vertices to be merged
        return G_prime, current_cut  # return the contracted graph and the current cut of the phase

    @staticmethod
    def __determine_most_tightly_connected_vertex(G, induced_ordering, previous_vertex):
        """
        Given an UndirectedGraph object, the list of the induced ordering of vertices computed from a
        single run of the minimum cut phase in the Stoer-Wagner algorithm, and the previous vertex added
        to the induced ordering, determines the vertex not in the input ordering that is most strongly
        connected to the vertices in the ordering
        """
        # compute the connection strengths
        G_prime = StoerWagner.__compute_connection_strengths(G, induced_ordering, previous_vertex)

        connection_strength_map = \
            dict({
                node: node.get_attribute_value(StoerWagner.CONNECTION_STRENGTH_ATTRIBUTE)
                for node in G_prime.get_nodeset()
                if node.get_name() not in induced_ordering
            })  # obtain the connection map

        # return the node with the strongest connection
        return max(connection_strength_map, key=connection_strength_map.get)

    @staticmethod
    def __compute_connection_strengths(G, induced_ordering, previous_vertex):
        """
        Given an UndirectedGraph object, the list of the induced ordering of vertices computed from a
        single run of the minimum cut phase in the Stoer-Wagner algorithm and the previous vertex added
        to the induced ordering, computes the connection strength of every vertex not in the induced ordering
        to the vertices in the ordering
        """
        # for edges incident to the previous vertex added to the induced ordering
        for edge in previous_vertex.get_incident_edges():
            other_node = edge.get_other_node(previous_vertex.get_name())  # get the other node object
            if other_node.get_name() not in induced_ordering:  # if the other node is not in the ordering
                other_node.set_attribute_value(
                    StoerWagner.CONNECTION_STRENGTH_ATTRIBUTE,
                    other_node.get_attribute_value(StoerWagner.CONNECTION_STRENGTH_ATTRIBUTE) + edge.get_weight()
                )  # add to the connection strength, the weight of the edge
        return G  # return the graph with the connection strength information

    @staticmethod
    def __initialize_connection_strengths(G):
        """
        Given an UndirectedGraph object, initializes the connection strength of every vertex in the graph
        to zero and returns the new graph
        """
        G_prime = G.__deepcopy__()  # construct a deepcopy of the graph
        # for every vertex in the graph, initialize the connection strength to zero
        for node in G_prime.get_nodeset(): node.add_attribute(StoerWagner.CONNECTION_STRENGTH_ATTRIBUTE, float(0))
        return G_prime  # return the new graph

    @staticmethod
    def __get_merge_nodelist(induced_ordering):
        """
        Given a list of the induced ordering of vertices computed from a single run of the minimum cut
        phase in the Stoer-Wagner algorithm, creates a set of nodes that are to be contracted at the
        end of the cut phase
        """
        duplicate = list(induced_ordering)  # create a copy of the list containing the induced ordering
        return {duplicate.pop(), duplicate.pop()}  # return the vertices corresponding to the s-t cut

    @staticmethod
    def __construct_current_cut(induced_ordering):
        """
        Given a list of the induced ordering of vertices computed from a single run of the minimum cut
        phase in the Stoer-Wagner algorithm, partitions and returns the vertices of the graph into two
        sets to represent the corresponding cut of the phase
        """
        duplicate = list(induced_ordering)  # create a copy of the list containing the induced ordering
        left_partition = {duplicate.pop()}  # create the left partition
        right_partition = set(duplicate)  # create the right partition
        return \
            tuple(
                (
                    StoerWagner.__unpack_node_names(left_partition),
                    StoerWagner.__unpack_node_names(right_partition)
                )
            )  # return the pair of partitions

    @staticmethod
    def __unpack_node_names(node_names):
        """
        Given a set of node names, creates and returns a new set of node names that have been post-process
        to remove the effects of graph contraction
        """
        return \
            set({
                unpacked_node_name
                for node_name in node_names
                for unpacked_node_name in node_name.split(StoerWagner.MERGED_NODE_NAME_DELIMITER)
            })  # create and return the set of unpacked node names

    @staticmethod
    def evaluate_cut_weight(G, cut):
        """
        Given a graph G represented as an UndirectedGraph object and a vertex set cut represented as a pair
        of sets of partitioned vertices, computes and returns the weight of the input cut
        """
        cut_weight = float(0)  # initialize the cut weight to zero
        left_node_names, right_node_names = cut  # unpack the partitioned vertex sets
        for edge in G.get_edges():  # for every edge in the input graph
            # if the edge connects two vertices from either of the sets
            if ((edge.get_first_incident_node().get_name() in left_node_names and
                    edge.get_second_incident_node().get_name() in right_node_names) or
                    (edge.get_first_incident_node().get_name() in right_node_names and
                             edge.get_second_incident_node().get_name() in left_node_names)):
                cut_weight += edge.get_weight()  # add the weight of the edge to the cut weight
        return cut_weight  # return the accumulated cut weight

