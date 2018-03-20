class GraphProcessing:
    @staticmethod
    def construct_null_graph(num_nodes):
        return dict({node: dict({}) for node in range(num_nodes)})
