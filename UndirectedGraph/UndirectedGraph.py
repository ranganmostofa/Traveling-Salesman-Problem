from Node import Node
from Edge import Edge
from GraphProcessing import GraphProcessing


class UndirectedGraph:
    """
    General-purpose UndirectedGraph class for the UndirectedGraph module
    """
    def __init__(self, nodeset):
        """
        Constructor for the UndirectedGraph class - used to initialize all necessary fields of the
        UndirectedGraph object
        """
        self.nodeset = nodeset  # initialize all necessary fields

        self.__check_validity()  # check if graph is valid - throws exception if not

    def __str__(self):
        """
        Returns a neatly formatted string representation of the UndirectedGraph object
        """
        # string representation includes values of all inner fields
        return "Nodeset: " + "\n".join([node.__str__() for node in self.nodeset]) + "\n"

    def __hash__(self):
        """
        Returns the hashcode of the UndirectedGraph object
        """
        return hash(str(self))  # use the __str__ method to obtain the hashcode

    def __eq__(self, other):
        """
        Given an UndirectedGraph object, checks whether this UndirectedGraph object is equal to the input
        UndirectedGraph object - equality of two UndirectedGraph objects is defined in terms of equality
        of inner fields and not as identical objects in memory
        """
        # check equality of the nodesets
        return self.nodeset.__eq__(other.get_nodeset())

    def __deepcopy__(self):
        """
        Creates and returns a deepcopy of the current UndirectedGraph object - all internal nodes
        and edges and their respective internal fields are replicated without invoking an infinite
        recursive call
        """
        return UndirectedGraph.extract_edge_induced_subgraph(self, lambda edge: True)  # copy all edges

    def add_node_attributes(self, attribute_key, attribute_value):
        """
        Given an attribute key and the corresponding attribute value, adds the key-value pair to the
        attributes registry of each of the nodes in the nodeset of the graph
        """
        G_prime = self.__deepcopy__()  # create a deepcopy of the undirected graph
        for node in G_prime.get_nodeset():  # for every node in the graph
            # add the attribute key-value pair to the attributes registry of the node
            node.add_attribute(attribute_key, attribute_value)
        return G_prime  # return the modified graph

    def add_edge_attributes(self, attribute_key, attribute_value):
        """
        Given an attribute key and the corresponding attribute value, adds the key-value pair to the
        attributes registry of each of the edges in the graph
        """
        G_prime = self.__deepcopy__()  # create a deepcopy of the undirected graph
        for edge in G_prime.get_edges():  # for every edge in the graph
            # add the attribute key-value pair to the attributes registry of the edge
            edge.add_attribute(attribute_key, attribute_value)
        return G_prime  # return the modified graph

    def add_node(self, node):
        """
        Given a Node object, adds the input to the nodeset of the undirected graph
        """
        self.nodeset.add(node)  # add the input node to the nodeset

        self.__check_validity()  # check if graph is valid - throws exception if not

    def add_edge(self, weight, attributes, first_incident_node, second_incident_node):
        """
        Given the necessary inner fields of an Edge object, creates the Edge object and connects the
        source and terminal nodes using this edge. Returns the created edge object.
        """
        # if the first incident node is not in the nodeset
        if first_incident_node.get_name() not in self.get_node_names():
            self.add_node(first_incident_node)  # add the first incident node

        # if the second incident node is not in the nodeset
        if second_incident_node.get_name() not in self.get_node_names():
            self.add_node(second_incident_node)  # add the second incident node

        edge = Edge(weight, attributes, first_incident_node, second_incident_node)  # create the Edge object

        first_incident_node.add_incident_edge(edge)  # connect the first and second incident nodes using the edge
        second_incident_node.add_incident_edge(edge)

        self.__check_validity()  # check if graph is valid - throws exception if not

        return edge  # return the newly added edge

    def contains_edge(self, node, other_node):
        """

        :param node:
        :param other_node:
        :return:
        """
        return \
            {node.get_name(), other_node.get_name()} in \
            list([
                {edge.get_first_incident_node().get_name(), edge.get_second_incident_node().get_name()}
                for edge in self.get_edges()
            ])

    def get_nodeset(self):
        """
        Returns the nodeset of the undirected graph
        """
        return set(self.nodeset)  # return the nodeset

    def get_node_names(self):
        """
        Returns a set of names belonging to the nodes in the nodeset of the undirected graph
        """
        return set({node.get_name() for node in self.get_nodeset()})  # return the set of names

    def get_edge(self, node, other_node):
        """

        :param node:
        :param other_node:
        :return:
        """
        if self.contains_edge(node, other_node):
            return \
                {
                    edge
                    for edge in self.get_edges()
                    if {
                           node.get_name(),
                           other_node.get_name()
                       } ==
                       {
                           edge.get_first_incident_node().get_name(),
                           edge.get_second_incident_node().get_name()
                       }
                }.pop()
        raise Exception("Invalid request: desired edge does not exist.")

    def get_edges(self):
        """
        Returns a set of the edges in the undirected graph
        """
        return \
            set({
                edge
                for node in self.nodeset
                for edge in node.get_incident_edges()
            })

    def set_nodeset(self, nodeset):
        """
        Given a set of nodes, sets the current nodeset as the input
        """
        self.nodeset = set(nodeset)  # overwrite the existing nodeset with the input nodeset

        self.__check_validity()  # check if graph is valid - throws exception if not

    @staticmethod
    def undirected_graph_to_dictionary_form(G):
        """
        Given an UndirectedGraph object, returns a dictionary representation of the input graph
        """
        G_dict = dict()  # initialize the dictionary
        for node in G.get_nodeset():  # for every node
            G_dict[node.get_name()] = dict()  # initialize the inner dictionary
            for edge in node.get_incident_edges():  # for every edge
                other_node = {node for node in edge.get_incident_nodes() if not node.get_name().__eq__()}.pop()
                # add the edge, including the edge weight
                G_dict[node.get_name()][other_node.get_name()] = edge.get_weight()
        return G_dict  # return the populated adjacency matrix representation

    @staticmethod
    def dictionary_to_undirected_graph_form(G):
        """
        Given a graph represented as a dictionary, returns the same graph as an UndirectedGraph object
        """
        # produce a set of disconnected Node objects with node names from the input graph
        nodeset = {Node(str(node_name), dict(), set()) for node_name in G.keys()}
        G_prime = UndirectedGraph(nodeset)  # create the corresponding null graph

        # for every node name
        for first_incident_node_name in G.keys():
            # for every adjacent node name
            for second_incident_node_name, weight in G[first_incident_node_name].items():
                first_incident_node_name = str(first_incident_node_name)
                second_incident_node_name = str(second_incident_node_name)
                # if the edge has not already been added
                if {first_incident_node_name, second_incident_node_name} \
                        not in [{edge.get_first_incident_node().get_name(), edge.get_second_incident_node().get_name()}
                            for edge in G_prime.get_edges()]:
                    # get the first node object
                    first_incident_node = \
                        GraphProcessing.search_node_names(G_prime.get_nodeset(), first_incident_node_name).pop()
                    # get the second node object
                    second_incident_node = \
                        GraphProcessing.search_node_names(G_prime.get_nodeset(), second_incident_node_name).pop()

                    # add the edge
                    G_prime.add_edge(weight, dict(), first_incident_node, second_incident_node)

        return G_prime  # return the UndirectedGraph object

    def extract_edge_induced_subgraph(self, predicate):
        """
        Given a predicate that accepts Edge objects as inputs, returns the edge-induced subgraph of the graph
        based on the set of edges filtered by the input predicate.

        NOTE: An edge-induced subgraph is defined here as a graph with a set of nodes exactly identical to
              the original set but with the filtered set of edges. As a result, the subgraph may contain
              disconnected nodes. However, as an added bonus of using this convention, this method may
              also be used to efficiently produce deep copies of an existing graph
        """
        # initialize the new nodeset as sets containing disconnected copies of the original nodes
        nodeset = {node.produce_duplicate_disconnected_node() for node in self.get_nodeset()}

        # create a null graph using the nodeset constructed above
        G_prime = UndirectedGraph(nodeset)

        # for every edge in the original graph
        for edge in self.get_edges():
            if predicate(edge):  # if the edge is not filtered out
                G_prime = UndirectedGraph.__induced_subgraph_helper(G_prime, edge)

        return G_prime  # return the subgraph

    def extract_node_induced_subgraph(self, predicate):
        """

        :param predicate:
        :return:
        """
        nodeset = {node.produce_duplicate_disconnected_node() for node in self.get_nodeset() if predicate(node)}

        G_prime = UndirectedGraph(nodeset)

        for edge in self.get_edges():
            if edge.get_first_incident_node().get_name() in G_prime.get_node_names():
                if edge.get_second_incident_node().get_name() in G_prime.get_node_names():
                    G_prime = UndirectedGraph.__induced_subgraph_helper(G_prime, edge)
        return G_prime

    @staticmethod
    def __induced_subgraph_helper(G, edge):
        """

        :param G:
        :param edge:
        :return:
        """
        first_incident_node = \
            GraphProcessing.search_node_names(
                G.get_nodeset(),
                edge.get_first_incident_node().get_name()
            ).pop()  # obtain the disconnected copy of the first incident node

        second_incident_node = \
            GraphProcessing.search_node_names(
                G.get_nodeset(),
                edge.get_second_incident_node().get_name()
            ).pop()  # obtain the disconnected copy of the second incident node

        G.add_edge(
            edge.get_weight(),
            dict(edge.get_attributes()),
            first_incident_node,
            second_incident_node
        )  # create and add the duplicate edge to the subgraph

        return G

    def contract_graph(self, node_names, merged_node_name):
        """

        :param node_names:
        :param merged_node_name:
        :return:
        """
        G_prime = self.extract_node_induced_subgraph(lambda node: node.get_name() not in node_names)
        merged_node = Node(merged_node_name, dict(), set())
        G_prime.add_node(merged_node)
        for node_name in node_names:
            node = GraphProcessing.search_node_names(self.get_nodeset(), node_name).pop()
            for edge in node.get_incident_edges():
                other_node = edge.get_other_node(node_name)
                if other_node.get_name() not in node_names:
                    G_prime_node = GraphProcessing.search_node_names(G_prime.get_nodeset(), other_node.get_name()).pop()
                    if G_prime.contains_edge(merged_node, G_prime_node):
                        G_prime_edge = G_prime.get_edge(merged_node, G_prime_node)
                        G_prime_edge.set_weight(G_prime_edge.get_weight() + edge.get_weight())
                    else:
                        G_prime.add_edge(edge.get_weight(), dict(), merged_node, G_prime_node)
        return G_prime

    def __has_conflicting_node_names(self):
        """
        Returns True if the graph nodes have conflicting names and False otherwise
        """
        # check length of sets to determine if overlap exists
        return len({node.get_name() for node in self.get_nodeset()}) != len(self.get_nodeset())

    def __has_multiple_edges(self):
        """
        Returns True if the graph has multiple edges originating from and leading to the same node and False
        otherwise
        """
        return \
            len(
                list(
                    [
                        tuple((edge.get_first_incident_node().get_name(), edge.get_second_incident_node().get_name()))
                        for edge in self.get_edges()
                    ]  # the length of the list which allows duplicates...
                )
            ) != \
            len(
                set(
                    {
                        tuple((edge.get_first_incident_node().get_name(), edge.get_second_incident_node().get_name()))
                        for edge in self.get_edges()
                    }  # ...should equal the length of the set that does not allow duplicates
                )
            )  # return True if the two data structures are equal in size and False otherwise

    def __check_validity(self):
        """
        Throws an exception if:

        (1) Nodes have conflicting names
        (2) Multiple edges exist

        Method should be called after every mutation
        """
        if self.__has_conflicting_node_names():  # if the graph has nodes with conflicting node names
            raise Exception("Error: Nodes have conflicting names")  # raise an exception
        if self.__has_multiple_edges():  # if the graph has nodes with multiple edges
            raise Exception("Error: Multiple edges exist")  # raise an exception

