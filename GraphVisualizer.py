from graphviz import *


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

