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
    def extract_edge_induced_subgraph(G, predicate):
        """
        Given an UndirectedGraph object and a predicate that accepts Edge objects as inputs, returns the
        edge-induced subgraph of the input graph based on the set of edges filtered by the input predicate.

        NOTE: An edge-induced subgraph is defined here as a graph with a set of nodes exactly identical to
              the original set but with the filtered set of edges. As a result, the subgraph may contain
              disconnected nodes. However, as an added bonus of using this convention, this method may
              also be used to efficiently produce deep copies of an existing graph
        """
        # initialize the new nodeset as sets containing disconnected copies of the original nodes
        nodeset = {GraphProcessing.produce_duplicate_disconnected_node(node) for node in G.get_nodeset()}

        # create a null graph using the nodeset constructed above
        G_prime = UndirectedGraph(nodeset)

        # for every edge in the original graph
        for edge in G.get_edges():
            if predicate(edge):  # if the edge is not filtered out
                first_incident_node = \
                    GraphProcessing.search_node_names(
                        G_prime.get_nodeset(),
                        edge.get_first_incident_node().get_name()
                    ).pop()  # obtain the disconnected copy of the first incident node

                second_incident_node = \
                    GraphProcessing.search_node_names(
                        G_prime.get_nodeset(),
                        edge.get_second_incident_node().get_name()
                    ).pop()  # obtain the disconnected copy of the second incident node

                G_prime.add_edge(
                    edge.get_weight(),
                    dict(edge.get_attributes()),
                    first_incident_node,
                    second_incident_node
                )  # create and add the duplicate edge to the subgraph

        return G_prime  # return the subgraph

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

