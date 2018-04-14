from GraphProcessing import GraphProcessing


class DataIO:
    """

    """
    @staticmethod
    def read_graph(filename):
        """

        :param filename:
        :return:
        """
        with open(filename, 'r') as file:
            num_nodes, num_edges = DataIO.__preprocess_line(file.readline())
            graph = GraphProcessing.construct_null_graph(num_nodes)
            for line in file.readlines():
                preprocessed_line = DataIO.__preprocess_line(line)
                if preprocessed_line:
                    source_node, terminal_node, weight = preprocessed_line
                    graph[source_node][terminal_node] = weight
                    graph[terminal_node][source_node] = weight
            return graph

    @staticmethod
    def write_graph(graph, filename):
        """

        :param graph:
        :param filename:
        :return:
        """
        with open(filename, 'w') as file:
            num_nodes, num_edges = GraphProcessing.compute_num_nodes(graph), GraphProcessing.compute_num_edges(graph)
            file.write(" ".join(list([str(num_nodes), str(num_edges)])) + "\n")
            for source_node in graph.keys():
                for terminal_node, weight in graph[source_node].items():
                    file.write(" ".join(list([str(source_node), str(terminal_node), str(weight)])) + "\n")

    @staticmethod
    def __preprocess_line(line):
        """

        :param line:
        :return:
        """
        return [int(element) for element in line.lstrip().rstrip().split()]

