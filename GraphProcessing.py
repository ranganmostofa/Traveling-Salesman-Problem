class GraphProcessing:
    @staticmethod
    def construct_null_graph(num_nodes):
        return dict({node: dict({}) for node in range(num_nodes)})

    @staticmethod
    def compute_num_nodes(graph):
        return len(graph.keys())

    @staticmethod
    def compute_num_edges(graph):
        return sum([len(graph[source_node].keys()) for source_node in graph.keys()]) / 2

