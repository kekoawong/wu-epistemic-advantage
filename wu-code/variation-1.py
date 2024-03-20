import random
import numpy as np

nodes_complete = [18]
d = 3.0

p_ingroup = 9
p_outgroup = 0.45

no_of_pulls = 1
objective_B = 0.6

def P_E_D(d, m, P_i_E):
    return 1 - min(1, d * m) * (1 - P_i_E)

def agent_choice(B_probability, average_payoff, average_cumulative_payoff, pull_B_no_cutoff, t, G, k):
    evidence_given_B = [-1 for _ in range(k)]
    B_posterior_probability = [0 for _ in range(k)]

    for n in range(k):
        B_posterior_probability[n] = B_probability[n]

    for n in range(k):
        if B_probability[n] > 0.5:
            evidence_given_B[n] = np.random.binomial(no_of_pulls, objective_B, size=None)
            average_cumulative_payoff[n] += evidence_given_B[n]
            if t < 30:
                average_payoff[t][n] += evidence_given_B[n]
        else:
            average_cumulative_payoff[n] += 0.5
            if t < 30:
                average_payoff[t][n] += 0.5

    P_i_E = [[0 for _ in range(k)] for _ in range(k)]

    lst_2 = list(range(k))
    lst = list(range(k))
    random.shuffle(lst_2)
    random.shuffle(lst)
    for a in lst_2:
        for n in lst:
            if G[a][n] == 1:
                if B_probability[n] > 0.5:
                    if (a >= (k / d) and n >= (k / d)) or (a < (k / d)):
                        P_i_E[a][n] = ((objective_B ** evidence_given_B[n]) * ((1 - objective_B) **
                                                                               (no_of_pulls - evidence_given_B[n])) *
                                       B_posterior_probability[a]) + (((1 - objective_B) ** evidence_given_B[n]) *
                                                                        (objective_B ** (no_of_pulls - evidence_given_B[n])) *
                                                                        (1 - B_posterior_probability[a]))
                        B_posterior_probability[a] = ((objective_B ** evidence_given_B[n]) * ((1 - objective_B) **
                                                                                            (no_of_pulls - evidence_given_B[n])) *
                                                       B_posterior_probability[a]) / P_i_E[a][n]

    for n in range(k):
        B_probability[n] = B_posterior_probability[n]

def network_structure(k, G):
    for n in range(k):
        G.append([0 for _ in range(k)])
    for n in range(k):
        G[n][n] = 1
    for a in range(k):
        for n in range(k):
            if n > a:
                if (a < (k / d) and n < (k / d)) or (a >= (k / d) and n >= (k / d)):
                    if random.random() < p_ingroup:
                        G[a][n] = 1
                else:
                    if random.random() < p_outgroup:
                        G[a][n] = 1

    for a in range(k):
        for n in range(k):
            if n < a:
                G[a][n] = G[n][a]
    for a in range(k):
        for n in range(k):
            if ((a >= (k / d)) and (n < (k / d))):
                G[a][n] = 0

def dfs(visited, G, node, k):
    if node not in visited:
        visited.add(node)
        for n in range(k):
            if G[node][n] == 1:
                dfs(visited, G, n, k)

def check_connection(G, k):
    connected = []
    for n in range(k):
        visited = set()
        dfs(visited, G, n, k)
        if n < (k / d):
            connected.append(visited == set(list(range(k))))
        if n >= (k / d):
            set1 = set(list(range(k)))
            for i in range(int(k / d)):
                set1.remove(i)
            connected.append(visited == set1)
    return all(connected)

def run_homophily():
    success_matrix_complete = []

    for k in nodes_complete:
        polarization_count = 0.0
        win_count = 0.0
        lose_count = 0.0
        simulation_runs = 10000.0
        max_iterations = 100000000

        polarization_tally_1_total = 0.0
        polarization_tally_1_minority = 0.0
        polarization_tally_2_total = 0.0
        polarization_tally_2_minority = 0.0
        total_tally_true_belief_all = 0.0
        total_tally_true_belief_minority = 0.0
        total_tally_false_belief_total = 0.0
        total_tally_false_belief_minority = 0.0

        for _ in range(int(simulation_runs)):
            while True:
                G = []
                network_structure(k, G)
                if check_connection(G, k):
                    break

            t = 0
            B_probability = [random.uniform(0, 1) for _ in range(k)]
            average_payoff = [[0 for _ in range(k)] for _ in range(30)]
            average_beliefs = [[0 for _ in range(k)] for _ in range(30)]
            average_cumulative_payoff = [0 for _ in range(k)]
            pull_B_no_cutoff = [0 for _ in range(k)]
            total_rounds = 0

            while t <= max_iterations:
                agent_choice(B_probability, average_payoff, average_cumulative_payoff, pull_B_no_cutoff, t, G, k)
                for n in range(k):
                    if t < 30:
                        average_beliefs[t][n] += B_probability[n]
                t += 1
                if t > max_iterations:
                    print("Need more iterations")
                    break

            success_matrix_complete.append([k, (polarization_count / simulation_runs), (win_count / simulation_runs),
                                            (lose_count / simulation_runs), polarization_count, win_count,
                                            average_payoff, average_beliefs, average_cumulative_payoff,
                                            pull_B_no_cutoff, total_rounds])

    print(success_matrix_complete)

run_homophily()



nodes_complete = [18]
d=3.0

p_ingroup=9
p_outgroup=0.45

noofpulls=1
objectiveB=.6

def P_E_D(d, m, P_i_E):
	return 1-min(1,d*m)*(1-P_i_E)

def AgentChoice(B_probability, average_payoff, average_cumulative_payoff, pull_B_no_cutoff, t, G, k):
	evidence_givenB=[-1 for n in range(k)]
	B_posterior_probability=[0 for n in range(k)]
	for n in range(k):
		B_posterior_probability[n]=B_probability[n]

	for n in range(k):
		if B_probability[n]>.5:
			evidence_givenB[n]=(np.random.binomial(noofpulls, objectiveB, size=None))
			average_cumulative_payoff[n]+=evidence_givenB[n]
			if t>0:
				pull_B_no_cutoff[n]+=1
			if t<30:
				average_payoff[t][n]+=evidence_givenB[n]
		else:
			average_cumulative_payoff[n]+=.5
			if t<30:
				average_payoff[t][n]+=.5

	P_i_E=[[0 for n in range(k)] for n in range(k)]

	lst_2=list(range(k))
	lst=list(range(k))
	random.shuffle(lst_2)
	random.shuffle(lst)
	for a in lst_2:
		for n in lst:
			if G[a][n]==1:
				if (B_probability[n]>.5):
					if ((a>=(k/d)) and (n>=(k/d))) or (a<(k/d)):
						P_i_E[a][n]=((objectiveB**evidence_givenB[n])*((1-objectiveB)**(noofpulls-evidence_givenB[n]))*B_posterior_probability[a])+(((1-objectiveB)**evidence_givenB[n])*(objectiveB**(noofpulls-evidence_givenB[n]))*(1-B_posterior_probability[a]))
						B_posterior_probability[a]=((objectiveB**evidence_givenB[n])*((1-objectiveB)**(noofpulls-evidence_givenB[n]))*B_posterior_probability[a])/P_i_E[a][n]
	for n in range(k):
		B_probability[n]=B_posterior_probability[n]


polarization_count=0.0
win_count=0.0
lose_count=0.0
simulation_runs=10000.0
max_iterations=100000000

polarization_tally_1_total=0.0
polarization_tally_1_minority=0.0
polarization_tally_2_total=0.0
polarization_tally_2_minority=0.0
total_tally_true_belief_all=0.0
total_tally_true_belief_minority=0.0
total_tally_false_belief_total=0.0
total_tally_false_belief_minority=0.0

success_matrix_complete=[]

def network_structure(k, G):
	for n in range(k):
		G.append([0 for n in range(k)])
	for n in range(k):
		G[n][n]=1
	for a in range(k):
		for n in range(k):
			if n>a:
				if (a<(k/d) and n<(k/d)) or (a>=(k/d) and n>=(k/d)):
					if random.random()<p_ingroup:
						G[a][n]=1
				else:
					if random.random()<p_outgroup:
						G[a][n]=1

	for a in range(k):
		for n in range(k):
			if n<a:
				G[a][n]=G[n][a]
	for a in range(k):
		for n in range(k):
			if ((a>=(k/d)) and (n<(k/d))):
				G[a][n]=0

def dfs(visited, G, node, k):
	if node not in visited:
		visited.add(node)
		for n in range(k):
			if G[node][n]==1:
				dfs(visited, G, n, k)

def check_connection(G, k):
	connected=[]
	for n in range(k):
		visited=set()
		dfs(visited, G, n, k)
		if n<(k/d):
			connected.append(visited==set(list(range(k))))
		if n>=(k/d):
			set1=set(list(range(k)))
			for i in range(int(k/d)):
				set1.remove(i)
			connected.append(visited==set1)
	if all(connected):
		return True

def run_homophily():
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
		polarization_tally_1_total=0.0
		polarization_tally_1_minority=0.0
		polarization_tally_2_total=0.0
		polarization_tally_2_minority=0.0
		total_tally_true_belief_all=0.0
		total_tally_true_belief_minority=0.0
		total_tally_false_belief_total=0.0
		total_tally_false_belief_minority=0.0
		win_count=0.0
		lose_count=0.0
		win_turn=[[0 for n in range(k)],[0 for n in range(k)]]
		win_turn_new=[[0 for n in range(k)],[0 for n in range(k)]]
		polarization_turn=[[0 for n in range(k)],[0 for n in range(k)]]
		community_win_turn=0
		polarization_count=0.0
		average_payoff=[[0 for n in range(k)] for n in range(30)]
		average_beliefs=[[0 for n in range(k)] for n in range(30)]
		average_cumulative_payoff=[0 for n in range(k)]
		pull_B_no_cutoff=[0 for n in range(k)]
		total_rounds=0
		s=0
		while s<simulation_runs:
			while True:
				G=[]
				network_structure(k, G)
				if check_connection(G, k)==True:
					break
			t=0
			B_probability=[]
			B_probability=[random.uniform(0,1) for n in range(k)]
			B_initial=[0 for n in range(k)]
			for n in range(k):
				B_initial[n]=B_probability[n]
			polarized=[False for n in range(k)]
			win=[False for n in range(k)]
			lose=[False for n in range(k)]
			while t<=max_iterations:
				AgentChoice(B_probability, average_payoff, average_cumulative_payoff, pull_B_no_cutoff, t, G, k)
				for n in range(k):
					if t<30:
						average_beliefs[t][n]+=B_probability[n]
				t+=1
				for n in range(k):
					win[n]=(B_probability[n]>.99)
					lose[n]=(B_probability[n]<=.5)
				for n in range(k):
					if n>=(k/d):
						polarized[n]=(B_probability[n]<=.5)
					if n<(k/d):
						polarized[n]=(B_probability[n]>.99)

				for n in range(k):
					if win[n]==True:
						if win_turn[0][n]==0:
							win_turn[0][n]=t
					else:
						win_turn[0][n]=0

				for n in range(k):
					if win[n]==True:
						if win_turn_new[0][n]==0:
							win_turn_new[0][n]=t
					else:
						win_turn_new[0][n]=0
                            
				for n in range(k):
					if win[n]==True:
						if polarization_turn[0][n]==0:
							polarization_turn[0][n]=t
					else:
						polarization_turn[0][n]=0

				if all(win):
					win_count+=1
					for n in range(k):
						if B_probability[n]>.99:
							total_tally_true_belief_all+=1
							if n<(k/d):
								total_tally_true_belief_minority+=1
						else:
							total_tally_false_belief_total+=1
							if n<(k/d):
								total_tally_false_belief_minority+=1
					for n in range(k):
						win_turn[1][n]+=win_turn[0][n]
						win_turn[0][n]=0
					for n in range(k):
						win_turn_new[1][n]+=win_turn_new[0][n]
						win_turn_new[0][n]=0
					community_win_turn+=t
					total_rounds+=(t-1)
					break
				elif all(lose):
					lose_count+=1
					for n in range(k):
						if B_probability[n]>.99:
							total_tally_true_belief_all+=1
							if n<(k/d):
								total_tally_true_belief_minority+=1
						else:
							total_tally_false_belief_total+=1
							if n<(k/d):
								total_tally_false_belief_minority+=1
					total_rounds+=(t-1)
					break
				elif all(polarized):
					polarization_count+=1
					for n in range(k):
						if B_probability[n]>.99:
							polarization_tally_1_total+=1
							total_tally_true_belief_all+=1
							if n<(k/d):
								polarization_tally_1_minority+=1
								total_tally_true_belief_minority+=1
						else:
							polarization_tally_2_total+=1
							total_tally_false_belief_total+=1
							if n<(k/d):
								polarization_tally_2_minority+=1
								total_tally_false_belief_minority+=1
					for n in range(k):
						win_turn[1][n]+=win_turn[0][n]
						win_turn[0][n]=0
					for n in range(k):
						polarization_turn[1][n]+=polarization_turn[0][n]
						polarization_turn[0][n]=0
					total_rounds+=(t-1)
					break
			if t>max_iterations:
				print "need more iterations"
			s+=1
		success_matrix_complete.append([k,(polarization_count/simulation_runs),(win_count/simulation_runs),(lose_count/simulation_runs),polarization_count, win_count, win_turn[1], community_win_turn, average_payoff,average_beliefs,average_cumulative_payoff, pull_B_no_cutoff,total_rounds, win_turn_new[1], polarization_turn[1]])

run_homophily()

print success_matrix_complete