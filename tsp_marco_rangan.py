from time import time
from gurobipy import *
from graphviz import *


class Node:
    """
    General-purpose Node class for the UndirectedGraph module
    """
    def __init__(self, name, attributes, incident_edges):
        """
        Constructor for the Node class - used to initialize all necessary fields of the Node object

        NOTE: The name field must be unique across all nodes and the attributes dictionary must not
        contain any object references
        """
        self.name = name  # initialize all necessary fields
        self.attributes = attributes
        self.incident_edges = incident_edges

    def __str__(self):
        """
        Returns a neatly formatted string representation of the Node object
        """
        # string representation includes values of all inner fields
        return \
            "Node Name: " + str(self.name) + "\n" + \
            "Node Attributes: " + str(self.attributes) + "\n" + \
            "Incident Edges: " + "\n".join([edge.__str__() for edge in self.incident_edges]) + "\n"

    def __hash__(self):
        """
        Returns the hashcode of the Node object
        """
        return hash(str(self))  # use the __str__ method to obtain the hashcode

    def __eq__(self, other):
        """
        Given a Node object, checks whether this Node object is equal to the input Node object - equality
        of two Node objects is defined in terms of equality of their names and not as identical objects
        in memory
        """
        # check equality of names since names are unique identifiers of nodes
        return self.name.__eq__(other.get_name())

    def add_attribute(self, attribute_key, attribute_value):
        """
        Given an attribute key and the corresponding attribute value, adds the key-value pair to the
        attributes registry of the node
        """
        self.set_attribute_value(attribute_key, attribute_value)  # record the input key-value pair

    def add_incident_edge(self, incident_edge):
        """
        Given an Edge object as input, adds the edge to the existing set of incident edges
        """
        self.incident_edges.add(incident_edge)  # append the input edge to the set of incident edges

    def remove_attribute(self, attribute_key):
        """
        Given an attribute key, removes the key-value pair from the attributes registry of the node
        """
        self.attributes.__delitem__(attribute_key)  # delete the input key-value pair

    def remove_incident_edge(self, other_node_name):
        """
        Given the name of an adjacent node, removes the edge leading to the input node, from the
        existing set of incident edges
        """
        # delete the input edge from the set of incident edges
        self.set_incident_edges(
            set(
                [
                    edge
                    for edge in self.incident_edges
                    if not (edge.get_first_incident_node().get_name().__eq__(other_node_name) or
                            edge.get_second_incident_node().get_name().__eq__(other_node_name))
                ]
            )
        )

    def get_name(self):
        """
        Returns the name of the node
        """
        return self.name  # return the name

    def get_attributes(self):
        """
        Returns the attributes of the node
        """
        return dict(self.attributes)  # return the attributes

    def get_attribute_value(self, attribute_key):
        """
        Given an attribute key, accesses and returns the corresponding attribute value
        """
        return self.attributes[attribute_key]  # return the attribute value

    def get_incident_edges(self):
        """
        Returns the set of incident edges of the node
        """
        return set(self.incident_edges)  # return the set of incident edges

    def set_name(self, name):
        """
        Given a name, sets the current name of the node as the input
        """
        self.name = name  # overwrite the existing name with the input name

    def set_attributes(self, attributes):
        """
        Given a registry of attributes, sets the registry of current attributes of the node as the input
        """
        self.attributes = dict(attributes)  # overwrite the existing registry of attributes with the input attributes

    def set_attribute_value(self, attribute_key, attribute_value):
        """
        Given an attribute key-value pair, adds the pair to the registry. If an identical attribute key
        exists, the corresponding attribute value is overwritten with the input value
        """
        self.attributes[attribute_key] = attribute_value  # adds the input key-value pair to the registry

    def set_incident_edges(self, incident_edges):
        """
        Given a set of incident edges, sets the current set of incident edges as the input
        """
        self.incident_edges = set(incident_edges)  # overwrite the existing set of incident edges with the input set

    def produce_duplicate_disconnected_node(self):
        """
        Returns a disconnected duplicate of the current node
        """
        # retain the original name and attributes, but clear all outgoing and incoming edges
        return \
            Node(
                self.get_name(),
                dict(self.get_attributes()),
                set()
            )


class Edge:
    """
    General-purpose Edge class for the BipartiteGraph module

    NOTE: Multiple edges are not supported. As such, the incident node names uniquely identify an edge
    """
    def __init__(self, weight, attributes, first_incident_node, second_incident_node):
        """
        Constructor for the Edge class - used to initialize all necessary fields of the Edge object
        """
        self.weight = weight  # initialize all necessary fields
        self.attributes = attributes
        self.first_incident_node = first_incident_node
        self.second_incident_node = second_incident_node

    def __str__(self):
        """
        Returns a neatly formatted string representation of the Edge object
        """
        # string representation includes values of all inner fields
        return \
            "Edge Weight: " + str(self.weight) + "\n" + \
            "Edge Attributes: " + str(self.attributes) + "\n" + \
            "First Incident Node: \n" + str(self.first_incident_node.get_name()) + "\n" + \
            "Second Incident Node: \n" + str(self.second_incident_node.get_name()) + "\n"

    def __hash__(self):
        """
        Returns the hashcode of the Edge object
        """
        return hash(str(self))  # use the __str__ method to obtain the hashcode

    def __eq__(self, other):
        """
        Given an Edge object, checks whether this Edge object is equal to the input Edge object - equality
        of two Edge objects is defined in terms of equality of inner fields and not as identical objects
        in memory
        """
        # check equality of names and attributes as well as that of the incident Node objects
        return \
            self.weight == other.get_weight() and \
            self.attributes.__eq__(other.get_attributes()) and \
            self.get_incident_nodes().__eq__(other.get_incident_nodes())

    def add_attribute(self, attribute_key, attribute_value):
        """
        Given an attribute key and the corresponding attribute value, adds the key-value pair to the
        attributes registry of the edge
        """
        self.set_attribute_value(attribute_key, attribute_value)  # record the input key-value pair

    def remove_attribute(self, attribute_key):
        """
        Given an attribute key, removes the key-value pair from the attributes registry of the edge
        """
        self.attributes.__delitem__(attribute_key)  # delete the input key-value pair

    def get_weight(self):
        """
        Returns the weight value of the edge
        """
        return self.weight  # return the weight value

    def get_attributes(self):
        """
        Returns the attributes of the edge
        """
        return dict(self.attributes)  # return the attributes

    def get_attribute_value(self, attribute_key):
        """
        Given an attribute key, accesses and returns the corresponding attribute value
        """
        return self.attributes[attribute_key]  # return the attribute value

    def get_first_incident_node(self):
        """
        Returns the first incident node of the edge
        """
        return self.first_incident_node  # return the first incident node

    def get_second_incident_node(self):
        """
        Returns the second incident node of the edge
        """
        return self.second_incident_node  # return the second incident node

    def get_incident_nodes(self):
        """
        Returns the set of incident nodes of the edge
        """
        # return the set of incident edges
        return \
            {
                self.first_incident_node,
                self.second_incident_node
            }

    def get_other_node(self, node_name):
        """
        Given a node name, checks if the name belongs to a node incident to the edge and if so, returns
        the node object reference to the other incident node
        """
        # get the set of node names that are incident to this edge
        incident_node_names = {node.get_name() for node in self.get_incident_nodes()}
        if node_name in incident_node_names:  # if the input name belongs to a node that is incident to the edge
            return \
                GraphProcessing.search_node_names(
                    self.get_incident_nodes(),
                    incident_node_names.difference({node_name}).pop()
                ).pop()  # return the node object reference to the other incident node

    def set_weight(self, weight):
        """
        Given a weight value, sets the current weight value of the edge as the input
        """
        self.weight = weight  # overwrite the existing weight with the input weight value

    def set_attributes(self, attributes):
        """
        Given a registry of attributes, sets the registry of current attributes of the edge as the input
        """
        self.attributes = dict(attributes)  # overwrite the existing registry of attributes with the input attributes

    def set_attribute_value(self, attribute_key, attribute_value):
        """
        Given an attribute key-value pair, adds the pair to the registry. If an identical attribute key
        exists, the corresponding attribute value is overwritten with the input value
        """
        self.attributes[attribute_key] = attribute_value  # adds the input key-value pair to the registry

    def set_first_incident_node(self, first_incident_node):
        """
        Given a first incident Node object, sets the current first incident node of the edge as the input
        """
        # overwrite the existing first incident node with the input first incident Node object
        self.first_incident_node = first_incident_node

    def set_second_incident_node(self, second_incident_node):
        """
        Given a second incident Node object, sets the current second incident node of the edge as the input
        """
        # overwrite the existing second incident node with the input second incident Node object
        self.second_incident_node = second_incident_node


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

    def remove_node(self, node):
        """
        Given a node object, checks to see if the node is part of the nodeset of the graph and if so,
        removes the node from the graph
        """
        # if the node is a part of the graph
        if node.get_name() in self.get_node_names():
            for edge in node.get_incident_edges():  # for every edge incident to the input node
                other_node = edge.get_other_node(node.get_name())  # get the other incident node object
                if other_node.get_name() in self.get_node_names():  # if the other node is a part of the graph
                    self.remove_edge(tuple((node, other_node)))  # remove the edge
            self.set_nodeset(
                set({
                    vertex
                    for vertex in self.get_nodeset()
                    if not vertex.get_name().__eq__(node.get_name())
                })
            )  # remove the node from the graph's nodeset

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

    def remove_edge(self, node_pair):
        """
        Given a pair of node objects, checks if the nodes are contained in the graph and if so,
        removes the edge from the graph
        """
        node, other_node = node_pair  # unpack the nodes
        # if the nodes are part of the graph
        if node.get_name() in self.get_node_names() and other_node.get_name() in self.get_node_names():
            node.remove_incident_edge(other_node.get_name())  # remove the incident edge object
            other_node.remove_incident_edge(node.get_name())  # references from both nodes

    def contains_edge(self, node, other_node):
        """
        Given two node objects, returns true if there exists an edge between the two objects and false otherwise
        """
        return \
            {node.get_name(), other_node.get_name()} in \
            list([
                {edge.get_first_incident_node().get_name(), edge.get_second_incident_node().get_name()}
                for edge in self.get_edges()
            ])  # return true if there exists an edge between the input nodes and false otherwise

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
        Given two nodes, returns the edge that connects them. Raises an exception if such an edge
        does not exist
        """
        # if there exists an edge between the two input nodes
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
                }.pop()  # return the edge
        # otherwise raise an exception
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
        Given a predicate that accepts Node objects as inputs, returns the node-induced subgraph of the graph
        based on the set of nodes filtered by the input predicate.
        """
        # construct the filtered nodeset
        nodeset = {node.produce_duplicate_disconnected_node() for node in self.get_nodeset() if predicate(node)}

        G_prime = UndirectedGraph(nodeset)  # create a new subgraph

        for edge in self.get_edges():  # for every edge in the original graph
            # if the first incident node is in the graph
            if edge.get_first_incident_node().get_name() in G_prime.get_node_names():
                # if the second incident node is also in the graph
                if edge.get_second_incident_node().get_name() in G_prime.get_node_names():
                    # add the edge to the subgraph
                    G_prime = UndirectedGraph.__induced_subgraph_helper(G_prime, edge)
        return G_prime  # return the subgraph

    @staticmethod
    def __induced_subgraph_helper(G, edge):
        """
        Helper function that adds a duplicate edge to the input graph and returns the modified graph.
        Useful for extracting subgraphs.
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
        Given a set of node names to merge and the final merged node name, contracts the nodes in the
        input set to a single node by carrying out the following steps:
        (1) Add node with the input merged node name
        (2) Delete nodes that were merged
        (3) Delete edges between nodes that were merged and
        (4) Any edges from the two vertices to a remaining vertex are replaced by an edge weighted by the sum
            of the weights of the previous two edges
        """
        merged_node = Node(merged_node_name, dict(), set())  # create the merged node
        self.add_node(merged_node)  # add the merged node to the graph
        for node_name in node_names:  # for every node in the merged node set
            # find the corresponding node in the graph
            node = GraphProcessing.search_node_names(self.get_nodeset(), node_name).pop()
            for edge in node.get_incident_edges():  # for every edge incident to this node
                other_node = edge.get_other_node(node_name)  # get the other node object
                if other_node.get_name() not in node_names:  # if the other node is also not being merged
                    if self.contains_edge(merged_node, other_node):  # if the graph already has the edge
                        new_edge = self.get_edge(merged_node, other_node)  # get the object reference to the edge
                        new_edge.set_weight(new_edge.get_weight() + edge.get_weight())  # update the weight
                    else:
                        # otherwise, create a new edge
                        self.add_edge(edge.get_weight(), dict(), merged_node, other_node)
                    self.remove_edge(tuple((node, other_node)))  # remove the old edge
            self.remove_node(node)  # remove the node from the graph

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


class GraphProcessing:
    """
    Class that houses static methods related to various graph processing algorithms
    """

    @staticmethod
    def has_attribute_key(graph_element, attribute_key):
        """
        Given a graph element and an attribute key, returns True if the graph element has an attribute
        field of input key and False otherwise
        """
        return attribute_key in graph_element.get_attributes().keys()  # return whether key is present

    @staticmethod
    def has_attribute_value(graph_element, attribute_key, attribute_value):
        """
        Given a graph element and an attribute key-value pair, returns True if the Node object possesses
        the input key-value pair and False otherwise
        """
        # return whether the pair is present
        return graph_element.get_attributes()[attribute_key] == attribute_value

    @staticmethod
    def search_graph_elements(graph_element_set, attribute_key, attribute_value):
        """
        Given a set of graph elements and an attribute key-value pair, returns a filtered set of graph
        elements that possess the input key-value pair
        """
        # return the filtered set of graph elements
        return \
            {
                graph_element for graph_element in graph_element_set
                if GraphProcessing.has_attribute_value(graph_element, attribute_key, attribute_value)
            }

    @staticmethod
    def search_node_names(nodeset, target_name):
        """
        Given a set of nodes, returns a filtered set of nodes that have names identical to the input name
        """
        # return the filtered set of nodes
        return \
            {
                node for node in set(nodeset)
                if node.get_name().__eq__(target_name)
            }

    @staticmethod
    def construct_null_graph(num_nodes):
        """
        Given the number of nodes, returns a null graph (represented using a dictionary) with
        {0, 1, ..., num_nodes - 1} as the nodeset
        """
        # return the graph represented using dictionary format
        return dict({node: dict({}) for node in range(num_nodes)})

    @staticmethod
    def compute_num_nodes(graph):
        """
        Given a graph represented using dictionary format, returns the number of nodes in the graph
        """
        return len(graph.keys())  # return the number of nodes in the graph

    @staticmethod
    def compute_num_edges(graph):
        """
        Given a graph represented using dictionary format, returns the number of edges in the graph
        """
        # return the number of edges
        return sum([len(graph[source_node].keys()) for source_node in graph.keys()]) / 2


class DataIO:
    """
    Class containing implementation of functions used to read and graphs from textfiles
    """
    @staticmethod
    def read_graph(filename):
        """
        Given a filename containing a graph, opens and reads the graph as a dictionary and returns it
        """
        with open(filename, 'r') as file:  # open the file
            # read the number of nodes and number of edges
            num_nodes, num_edges = DataIO.__preprocess_line(file.readline())
            graph = GraphProcessing.construct_null_graph(num_nodes)  # construct a null graph
            for line in file.readlines():  # for every line in the file
                preprocessed_line = DataIO.__preprocess_line(line)  # preprocess the line
                if preprocessed_line:  # if the preprocessed line is not a null string
                    # read the first and second node and the edge weight
                    source_node, terminal_node, weight = preprocessed_line
                    graph[source_node][terminal_node] = weight
                    graph[terminal_node][source_node] = weight
            return graph  # return the final graph

    @staticmethod
    def write_graph(graph, filename):
        """
        Given a graph represented as a dictionary and a filename, creates and opens a textfile with the
        same name as the input filename and stored the graph in the newly created textfile
        """
        with open(filename, 'w') as file:  # open the file
            # record the number of nodes and edges
            num_nodes, num_edges = GraphProcessing.compute_num_nodes(graph), GraphProcessing.compute_num_edges(graph)
            file.write(" ".join(list([str(num_nodes), str(num_edges)])) + "\n")
            for source_node in graph.keys():  # for every node in the graph
                # for every other node and corresponding weight
                for terminal_node, weight in graph[source_node].items():
                    # write the edge to the file as the first node, second node and edge weight
                    file.write(" ".join(list([str(source_node), str(terminal_node), str(weight)])) + "\n")

    @staticmethod
    def write_tour(graph, tsp_model, filename):
        """
        Given a graph represented as a dictionary, a gurobi model object and a filename, stores the optimal tour
        as computed by the input gurobi model to a textfile
        """
        with open(filename, 'w') as file:  # open the textfile
            for decision_variable in tsp_model.getVars():  # for every decision variable in the model
                if decision_variable.getAttr("X"):  # if the value is true
                    variable_name = decision_variable.getAttr("VarName")  # get the variable name
                    i, j = (int(num) for num in variable_name.split("_"))  # retrieve the node names
                    file.write(" ".join([str(i), str(j), str(graph[i][j])]) + "\n")  # store the edge in a new line
            # store the cost of the optimal tour as the final line
            file.write("The cost of the best tour is: " + str(tsp_model.getAttr("ObjVal")) + "\n")

    @staticmethod
    def __preprocess_line(line):
        """
        Given a line from a textfile containing a graph, preprocesses the line by removing the whitespaces
        around the line and splitting based on whitespace
        """
        return [int(element) for element in line.lstrip().rstrip().split()]  # preprocess the input line


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


class GraphVisualizer:
    """
    Class that houses code used to visualize graphs
    """
    @staticmethod
    def disp_graph(graph, output_filename):
        """
        Given a graph represented as a dictionary and an output filename, visualizes the graph and saves it
        as a png file
        """
        dot = Graph(name="Graph", format="png")  # instantiate a graph object
        for node in graph.keys():  # add nodes to the graph
            dot.node(str(node))
        for node in graph.keys():  # for every node in the input graph
            # for every other node in the input graph that the first node is connected to
            for other_node in graph[node].keys():
                dot.edge(str(node), str(other_node))  # create the edge
        dot.render(output_filename, view=True)  # visualize the graph and save it


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

