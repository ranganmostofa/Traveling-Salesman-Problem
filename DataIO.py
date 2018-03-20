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
            return graph

    @staticmethod
    def write_graph(graph, filename):
        """

        :param graph:
        :param filename:
        :return:
        """
        pass

    @staticmethod
    def __preprocess_line(line):
        """

        :param line:
        :return:
        """
        return [int(element) for element in line.lstrip().rstrip().split()]


from pprint import pprint

pprint(DataIO.read_graph('Data/att48.txt'))

