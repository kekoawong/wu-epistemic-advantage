from typing import Literal
import networkx as nx
import numpy as np
import random

# Define Parameters
num_agents = 3 # number of nodes in network, alternates between 3, 6, 12, 18
proportion_marginalized = 1/6 # % population marginalized, alternates between 1/6, 1/3, 1/2, 2/3
num_pulls = 1 # number of arm pulls, alternates between 1, 5, 10, 20
objective_b = 0.51 # actual probability of B arm yielding success, alternates between .51, .55, .6, .7, .8

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
    # experimental constants, put these on the outside
    num_pulls = 1
    success_rate = 0.51
    # run the experiments in all the nodes
    for _node, node_data in graph.nodes(data=True):
        # agent pulls the "a" bandit arm
        if node_data['a_success_rate'] > node_data['b_success_rate']:
            # agent won't have any new evidence gathered for b
            node_data['b_evidence'] = None

        # agent pulls the "b" bandit arm
        else:
            # agent collects evidence
            node_data['b_evidence'] = int(np.random.binomial(num_pulls, success_rate, size=None))

    # define function to calculate posterior belief
        def calculate_posterior(prior_belief: float, num_evidence: float) -> float:
            # Calculate likelihood, will be either the success rate
            pEH_likelihood = (objective_b ** num_evidence) * ((1 - objective_b) ** (num_pulls - num_evidence))
            
            # Calculate normalization constant
            pE_evidence = (pEH_likelihood * prior_belief) + ((1 - objective_b)**num_evidence) * (objective_b ** (num_pulls - num_evidence)) * (1 - prior_belief)

            # Calculate posterior belief using Bayes' theorem
            posterior = (pEH_likelihood * prior_belief) / pE_evidence
            
            return posterior
    
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
