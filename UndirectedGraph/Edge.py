from GraphProcessing import GraphProcessing


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

