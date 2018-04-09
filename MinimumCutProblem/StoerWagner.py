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

        """
        minimum_cut = tuple()
        minimum_cut_weight = float('inf')
        G_prime = G.__deepcopy__()
        while len(G_prime.get_nodeset()) > 1:
            G_prime, current_cut = StoerWagner.__minimum_cut_phase(G_prime, initial_node_name)
            current_cut_weight = StoerWagner.evaluate_cut_weight(G, current_cut)
            if current_cut_weight < minimum_cut_weight:
                minimum_cut = current_cut
                minimum_cut_weight = current_cut_weight
        return tuple(minimum_cut), float(minimum_cut_weight)

    @staticmethod
    def __minimum_cut_phase(G, initial_node_name):
        """

        :param G:
        :param initial_node_name:
        :return:
        """
        induced_ordering = list([initial_node_name])
        while set(induced_ordering) != G.get_node_names():
            print(str(len(induced_ordering)) + ": " + str(induced_ordering))
            next_vertex = StoerWagner.__determine_most_tightly_connected_vertex(G, induced_ordering)
            induced_ordering.append(next_vertex.get_name())
        merge_nodelist = StoerWagner.__get_merge_nodelist(induced_ordering)
        current_cut = StoerWagner.__construct_current_cut(induced_ordering)
        print("Current Cut: " + str(current_cut))
        print(len(induced_ordering))
        G_prime = G.merge_nodes(merge_nodelist, StoerWagner.MERGED_NODE_NAME_DELIMITER.join(merge_nodelist))
        return G_prime, current_cut

    @staticmethod
    def __determine_most_tightly_connected_vertex(G, induced_ordering):
        """

        :param G:
        :param induced_ordering:
        :return:
        """
        G_prime = StoerWagner.__compute_connection_strengths(G, induced_ordering)

        connection_strength_map = \
            dict({
                node: node.get_attribute_value(StoerWagner.CONNECTION_STRENGTH_ATTRIBUTE)
                for node in G_prime.get_nodeset()
            })

        return max(connection_strength_map, key=connection_strength_map.get)

    @staticmethod
    def __compute_connection_strengths(G, induced_ordering):
        """

        :param G:
        :param induced_ordering:
        :return:
        """
        G_prime = StoerWagner.__initialize_connection_strengths(G)
        for node in G_prime.get_nodeset():
            if node.get_name() not in induced_ordering:
                for edge in node.get_incident_edges():
                    other_node = edge.get_other_node(node.get_name())
                    if other_node.get_name() in induced_ordering:
                        node.set_attribute_value(
                            StoerWagner.CONNECTION_STRENGTH_ATTRIBUTE,
                            node.get_attribute_value(StoerWagner.CONNECTION_STRENGTH_ATTRIBUTE) + edge.get_weight()
                        )
        return G_prime

    @staticmethod
    def __initialize_connection_strengths(G):
        """

        :param G:
        :return:
        """
        G_prime = G.__deepcopy__()
        for node in G_prime.get_nodeset(): node.add_attribute(StoerWagner.CONNECTION_STRENGTH_ATTRIBUTE, float(0))
        return G_prime

    @staticmethod
    def __get_merge_nodelist(induced_ordering):
        """

        :param induced_ordering:
        :return:
        """
        duplicate = list(induced_ordering)
        return {duplicate.pop(), duplicate.pop()}

    @staticmethod
    def __construct_current_cut(induced_ordering):
        """

        :param induced_ordering:
        :return:
        """
        duplicate = list(induced_ordering)
        left_partition = {duplicate.pop()}
        right_partition = set(duplicate)
        return \
            tuple(
                (
                    StoerWagner.__unpack_node_names(left_partition),
                    StoerWagner.__unpack_node_names(right_partition)
                )
            )

    @staticmethod
    def __unpack_node_names(node_names):
        """

        :param node_names:
        :return:
        """
        return \
            set({
                unpacked_node_name
                for node_name in node_names
                for unpacked_node_name in node_name.split(StoerWagner.MERGED_NODE_NAME_DELIMITER)
            })

    @staticmethod
    def evaluate_cut_weight(G, cut):
        """

        :param G:
        :param cut:
        :return:
        """
        cut_weight = float(0)
        left_node_names, right_node_names = cut
        for edge in G.get_edges():
            if ((edge.get_first_incident_node().get_name() in left_node_names and
                    edge.get_second_incident_node().get_name() in right_node_names) or
                    (edge.get_first_incident_node().get_name() in right_node_names and
                             edge.get_second_incident_node().get_name() in left_node_names)):
                cut_weight += edge.get_weight()
        return cut_weight

