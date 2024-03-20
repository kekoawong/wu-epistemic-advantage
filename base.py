import networkx as nx 
import random
import numpy as np
from numpy import random

nodes_complete = [3, 6, 12, 18]

d: float = 1.5

noofpulls: int = 1
objectiveB: float = 0.51

def AgentChoice(B_probability: list[float], average_payoff: list[list[float]], average_cumulative_payoff: list[float], t: int, G: nx.Graph):
    evidence_givenB: list[int] = [-1 for _ in G.nodes()]
    B_posterior_probability: list[float] = [0 for _ in G.nodes()]
    
    for n in G.nodes():
        B_posterior_probability[n] = B_probability[n]
        
    for n in G.nodes():
        if B_probability[n] > 0.5:
            evidence_givenB[n] = int(np.random.binomial(noofpulls, objectiveB, size=None))
            average_cumulative_payoff[n] += evidence_givenB[n]
            if t < 30:
                average_payoff[t][n] += evidence_givenB[n]
        else:
            average_cumulative_payoff[n] += 0.5
            if t < 30:
                average_payoff[t][n] += 0.5

    P_i_E = [[0 for _ in G.nodes()] for _ in G.nodes()]
    
    lst_2 = list(G.nodes())
    lst = list(G.nodes())
    random.shuffle(lst_2)
    random.shuffle(lst)
    
    for a in lst_2:
        for n in lst:
            if B_probability[n] > 0.5:
                if ((a >= (len(lst) / d)) and (n >= (len(lst) / d))) or (a < (len(lst) / d)):
                    P_i_E[a][n] = ((objectiveB ** evidence_givenB[n]) * ((1 - objectiveB) ** (noofpulls - evidence_givenB[n])) * B_posterior_probability[a]) + (((1 - objectiveB) ** evidence_givenB[n]) * (objectiveB ** (noofpulls - evidence_givenB[n])) * (1 - B_posterior_probability[a]))
                    B_posterior_probability[a] = ((objectiveB ** evidence_givenB[n]) * ((1 - objectiveB) ** (noofpulls - evidence_givenB[n])) * B_posterior_probability[a]) / P_i_E[a][n]
    
    for n in G.nodes():
        B_probability[n] = B_posterior_probability[n]

def initialize_graph(numNodes: int):
    initialNodeData = {
        'probability': 0,
    }
    graph: nx.Graph = nx.complete_graph(numNodes)
    # Set the initial node data for each node
    for node in graph.nodes():
        graph.nodes[node].update(initialNodeData)

    return graph

def timestep():
    return

polarization_count = 0.0
win_count = 0.0
lose_count = 0.0
simulation_runs = 1000.0
max_iterations = 100000

polarization_tally_1_total = 0.0
polarization_tally_1_minority = 0.0
polarization_tally_2_total = 0.0
polarization_tally_2_minority = 0.0
total_tally_true_belief_all = 0.0
total_tally_true_belief_minority = 0.0
total_tally_false_belief_total = 0.0
total_tally_false_belief_minority = 0.0

success_matrix_complete = []

def run_complete():
    for k in nodes_complete:
        global polarization_count
        global win_count
        global lose_count
        global polarization_tally_1_total
        global polarization_tally_1_minority
        global polarization_tally_2_total
        global polarization_tally_2_minority
        global total_tally_true_belief_all
        global total_tally_true_belief_minority
        global total_tally_false_belief_total
        global total_tally_false_belief_minority
        
        polarization_tally_1_total = 0.0
        polarization_tally_1_minority = 0.0
        polarization_tally_2_total = 0.0
        polarization_tally_2_minority = 0.0
        total_tally_true_belief_all = 0.0
        total_tally_true_belief_minority = 0.0
        total_tally_false_belief_total = 0.0
        total_tally_false_belief_minority = 0.0
        win_count = 0.0
        lose_count = 0.0
        win_turn = [[0 for _ in range(k)], [0 for _ in range(k)]]
        community_win_turn = 0
        polarization_count = 0.0
        average_payoff = [[0 for _ in range(k)] for _ in range(30)]
        average_beliefs = [[0 for _ in range(k)] for _ in range(30)]
        average_cumulative_payoff = [0 for _ in range(k)]
        
        s = 0
        while s < simulation_runs:
            G = nx.complete_graph(k)
            t = 0
            B_probability = [random.uniform(0, 1) for _ in range(k)]
            B_initial = [0 for _ in range(k)]
            
            for n in G.nodes():
                B_initial[n] = B_probability[n]
                
            polarized = [False for _ in range(k)]
            win = [False for _ in range(k)]
            lose = [False for _ in range(k)]
            
            while t <= max_iterations:
                AgentChoice(B_probability, average_payoff, average_cumulative_payoff, t, G)
                
                for n in G.nodes():
                    if t < 30:
                        average_beliefs[t][n] += B_probability[n]
                
                t += 1
                
                for n in G.nodes():
                    win[n] = (B_probability[n] > 0.99)
                    lose[n] = (B_probability[n] <= 0.5)
                    
                    if n >= (k / d):
                        polarized[n] = (B_probability[n] <= 0.5)
                        
                    if n < (k / d):
                        polarized[n] = (B_probability[n] > 0.99)
                
                for n in G.nodes():
                    if win[n] == True:
                        if win_turn[0][n] == 0:
                            win_turn[0][n] = t
                    else:
                        win_turn[0][n] = 0
                
                if all(win):
                    win_count += 1
                    
                    for n in G.nodes():
                        if B_probability[n] > 0.99:
                            total_tally_true_belief_all += 1
                            
                            if n < (k / d):
                                total_tally_true_belief_minority += 1
                        else:
                            total_tally_false_belief_total += 1
                            
                            if n < (k / d):
                                total_tally_false_belief_minority += 1
                    
                    for n in G.nodes():
                        win_turn[1][n] += win_turn[0][n]
                        win_turn[0][n] = 0
                    
                    community_win_turn += t
                    break
                
                elif all(lose):
                    lose_count += 1
                    
                    for n in G.nodes():
                        if B_probability[n] > 0.99:
                            total_tally_true_belief_all += 1
                            
                            if n < (k / d):
                                total_tally_true_belief_minority += 1
                        else:
                            total_tally_false_belief_total += 1
                            
                            if n < (k / d):
                                total_tally_false_belief_minority += 1
                    break
                
                elif all(polarized):
                    polarization_count += 1
                    
                    for n in G.nodes():
                        if B_probability[n] > 0.99:
                            polarization_tally_1_total += 1
                            total_tally_true_belief_all += 1
                            
                            if n < (k / d):
                                polarization_tally_1_minority += 1
                                total_tally_true_belief_minority += 1
                        else:
                            polarization_tally_2_total += 1
                            total_tally_false_belief_total += 1
                            
                            if n < (k / d):
                                polarization_tally_2_minority += 1
                                total_tally_false_belief_minority += 1
                                
                    for n in G.nodes():
                        win_turn[1][n] += win_turn[0][n]
                        win_turn[0][n] = 0
                    break
                
            s += 1
            
        success_matrix_complete.append([k, (polarization_count / simulation_runs), (win_count / simulation_runs), (lose_count / simulation_runs), polarization_count, win_count, win_turn[1], community_win_turn, average_payoff, average_beliefs, average_cumulative_payoff])

run_complete()

print(success_matrix_complete)
