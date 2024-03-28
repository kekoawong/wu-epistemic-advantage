from typing import Literal
import networkx as nx
import numpy as np
import random

def initialize_graph(graphType: Literal['cycle', 'wheel', 'complete'], numNodes: int):
    graph: nx.Graph = nx.complete_graph(numNodes)
    # Initialize all the nodes to this initial data
    for node in graph.nodes():
        initial_data = {
            # bandit arm A is set to a 0.5 success rate in the decision process
            'a_success_rate': 0.5,
            # bandit arm B is a learned parameter for the agent. Initialize randomly
            'b_success_rate': random.uniform(0.01, 0.99),
            # agent evidence learned, will be used to update their belief and others in the network
            'b_evidence': None,
        }
        graph.nodes[node].update(initial_data)

    return graph

def timestep(graph: nx.Graph):
    # run the experiments in all the nodes
    for _node, node_data in graph.nodes(data=True):
        # agent pulls the "a" bandit arm
        if node_data['a_success_rate'] > node_data['b_success_rate']:
            # agent won't have any new evidence gathered for b
            node_data['b_evidence'] = None

        # agent pulls the "b" bandit arm
        else:
            # run the experiment
            num_pulls = 1
            success_rate = 0.51
            node_data['b_evidence'] = int(np.random.binomial(num_pulls, success_rate, size=None))

    # define function to calculate posterior belief
    def calculate_posterior(pH: float, pEH: float):
        if pH <= 0 or pH >= 1: 
            return pH
        pE = pEH * pH + (1 - pEH) * (1 - pH)
        return (pEH * pH) / pE
    
    # update the beliefs, based on evidence and neighbors
    for node, node_data in graph.nodes(data=True):
        neighbors = graph.neighbors(node)
        # update belief of "b" on own evidence gathered
        if node_data['b_evidence'] is not None:
            node_data['b_success_rate'] = calculate_posterior(node_data['b_success_rate'], node_data['b_evidence'])
        
        # update node belief of "b" based on evidence gathered by neighbors
        for neighbor_node in neighbors:
            neighbor_evidence = graph.nodes[neighbor_node]['b_evidence']
            if neighbor_evidence is not None:
                node_data['b_success_rate'] = calculate_posterior(node_data['b_success_rate'], neighbor_evidence)

    return graph

mainGraph = initialize_graph('wheel', 15)
timestamps = 50
for i in range(timestamps):
    timestep(mainGraph)
print(mainGraph)