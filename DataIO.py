from GraphProcessing import GraphProcessing


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

