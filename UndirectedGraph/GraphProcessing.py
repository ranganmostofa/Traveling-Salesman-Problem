from Node import Node
from UndirectedGraph import UndirectedGraph


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
    def produce_duplicate_disconnected_node(node):
        """
        Given a Node object, returns a disconnected duplicate of the input node
        """
        # retain the original name and attributes, but clear all outgoing and incoming edges
        return \
            Node(
                node.get_name(),
                dict(node.get_attributes()),
                set()
            )

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
        G_prime = UndirectedGraph()


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

