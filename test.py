from model import EpistemicAdvantageModel
import statistics
import networkx as nx

# Get all keys that have numerical values in the graph
model = EpistemicAdvantageModel()
initial = model.initialize_graph()
median_vals = []
numerical_keys = {key for node, data in initial.nodes(data=True) for key in data if isinstance(data[key], (int, float, complex))}
print("initial graph data", initial.nodes(data=True))
print("/n")
timesteps = 50
# print("b belief at before", [data['b_success_rate'] for node,data in initial.nodes(data=True)])
for _ in range(timesteps):
    updated_graph = model.timestep()
    timestep_medians = {}
    print("b belief at timestep", _, [data['b_success_rate'] for node,data in updated_graph.nodes(data=True)])
    for key in numerical_keys:
        values = [data[key] for node, data in updated_graph.nodes(data=True) if key in data and data[key] is not None]
        new_median = statistics.median(values) if values else 0
        timestep_medians[key] = new_median
    median_vals.append(timestep_medians)
# print("final graph data", updated_graph.nodes(data=True))
# print("median data", [data['b_success_rate'] for data in median_vals])
