from modelpy import Model
import networkx as nx
import random

# Inherit class from modelpy
# https://docs.python.org/3/tutorial/classes.html#inheritance
class MyModel(Model):
    def __init__(self):
        # Define Parameters
        self.num_nodes = 3
        self.graph_type = 'complete' # complete, wheel, or cycle
        
        # NOTE: This graph variable will not be loaded into the 
        # modelpy interface since it is not a string or number
        self.graph: nx.Graph = None

    def initialize_graph(self):
        # initialize graph shape
        if self.graph_type == 'complete':
            self.graph = nx.complete_graph(self.num_nodes)
        elif self.graph_type == 'cycle':
            self.graph = nx.cycle_graph(self.num_nodes)
        else:
            self.graph = nx.wheel_graph(self.num_nodes)
        
        # Initialize sample data for all nodes
        for node in self.graph.nodes():
            initial_data = {
                'data_value': random.uniform(1, 100),
            }
            self.graph.nodes[node].update(initial_data)

    def timestep(self):
        for _node, node_data in self.graph.nodes(data=True):
            # example mutate the node data
            node_data['data_value'] += node_data['data_value'] + 1