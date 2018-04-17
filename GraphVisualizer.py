from graphviz import *


class GraphVisualizer:
    @staticmethod
    def disp_graph(graph):
        dot = Graph(name="Graph", format="png")
        for node in graph.keys():
            dot.node(str(node))
        for node in graph.keys():
            for other_node in graph[node].keys():
                dot.edge(str(node), str(other_node))
        dot.render("test_graph.png", view=True)


