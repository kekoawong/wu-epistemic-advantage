from typing import Literal
import networkx as nx
import numpy as np
import random

def initialize_graph(graphType: Literal['cycle', 'wheel', 'complete'], numNodes: int):
    graph: nx.Graph = nx.complete_graph(numNodes)
    # Initialize all the nodes to this initial data
    for node in graph.nodes():
        initialNodeData = {
            # bandit arm A is set to a 0.5 success rate in the decision process
            'a_success_rate': 0.5,
            # bandit arm B is a learned parameter for the agent. Initialize randomly
            'b_success_rate': random.uniform(0.01, 0.99),
            # agent evidence learned, will be used to update their belief and others in the network
            'b_evidence': None,
        }
        graph.nodes[node].update(initialNodeData)

    return graph

def timestep(graph: nx.Graph):
    # run the experiments in all the nodes
    for _node, nodeData in graph.nodes(data=True):
        # agent pulls the "a" bandit arm
        if nodeData['a_success_rate'] > nodeData['b_success_rate']:
            # agent won't have any new evidence gathered for b
            nodeData['b_evidence'] = None

        # agent pulls the "b" bandit arm
        else:
            # run the experiment
            num_trials = 1
            success_rate = 0.51
            nodeData['b_evidence'] = int(np.random.binomial(num_trials, success_rate, size=None))

    # define function to calculate posterior belief
    def calculate_posterior(pH: float, pEH: float):
        pE = pEH * pH + (1 - pEH) * (1 - pH)
        return (pEH * pH) / pE
    
    # update the beliefs, based on evidence and neighbors
    for node, nodeData in graph.nodes(data=True):
        neighbors = graph.neighbors(node)
        # update belief of "b" on own evidence gathered
        if nodeData['b_evidence'] is not None:
            nodeData['b_success_rate'] = calculate_posterior(nodeData['b_success_rate'], nodeData['b_evidence'])
        
        # update node belief of "b" based on evidence gathered by neighbors
        for neighbor_node in neighbors:
            neighbor_evidence = graph.nodes[neighbor_node]['b_evidence']
            if neighbor_evidence is not None:
                nodeData['b_success_rate'] = calculate_posterior(nodeData['b_success_rate'], neighbor_evidence)

    return graph

# mainGraph = initialize_graph(15)
# timestamps = 50
# for i in range(timestamps):
#     timestep(mainGraph)
# print(mainGraph)