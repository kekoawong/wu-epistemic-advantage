# Getting Started
Currently, **Modelpy** is currently configured to work exclusively with graphical models (with a focus on bandits) using the [networkx](https://networkx.org/) package. 

We are working with researchers to add support for more models types across domains. To help develop this open source framework for your research domain, reach out here.

## Installation 
Make sure that you have configured your development environment to have the latest stable version of python and pip installed.
* [Pip Documentation](https://pip.pypa.io/en/stable/installation/)
* [Python Documentation](https://www.python.org/)

In your project directory, run the following command to install modelpy. 

```bash
pip add modelpy
```

## Create your model
Once you have installed modelpy, you can create your model by implementing the following steps:

### 1: Create a **model.py** file
Create a file named **model.py** file in the root/main directory of your project.

### 2: Import modules and define class
You will need to inherit the **Model** class from the modelpy module. To learn more about class inheritance, view the [python documentation](https://docs.python.org/3/tutorial/classes.html#inheritance).

> We will also be importing [Networkx](https://networkx.org/) to work with graph data structures. You will need to install this module using pip if you are building a graphical model.

```python
from modelpy import Model
import networkx as nx

# Inherit class from modelpy
# https://docs.python.org/3/tutorial/classes.html#inheritance
class MyModel(Model):
    ...
```

### 3: Define the `__init__` function. 
This will define your initialization parameters. Only the parameters that are strings or numbers will be editable in the modelpy interface.

```python
class MyModel(Model):
    def __init__(self):
        # Define Parameters
        self.num_nodes = 3
        self.graph_type = 'complete' # example stuctures like complete, wheel, or cycle
        
        # NOTE: This graph variable will not be loaded into the 
        # modelpy interface since it is not a string or number
        self.graph: nx.Graph = None
```

### 4: Define the `initialize_graph` function. 
This will define how a graph is initialized or reset.
the modelpy interface.

```python
class MyModel(Model):
    # __init__ function defined here
    ...

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
                'data_value': 0,
            }
            self.graph.nodes[node].update(initial_data)
```

### 5: Define the `timestep` function. 
This will define the logic that your model will perform at every timestep.

```python
class MyModel(Model):
    # __init__ and initialize_graph function defined here
    ...
    def timestep(self):
        for _node, node_data in self.graph.nodes(data=True):
            # example mutate the node data
            node_data['data_value'] += node_data['data_value'] + 1
```

### 6: Review
Now, your **model.py** file should look something like the following:

```python
from modelpy import Model
import networkx as nx

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
                'data_value': 0,
            }
            self.graph.nodes[node].update(initial_data)

    def timestep(self):
        for _node, node_data in self.graph.nodes(data=True):
            # example mutate the node data
            node_data['data_value'] += node_data['data_value'] + 1
```

## Run your model
Now that you have successfully created your model, you can now run it using the following code:
```python
new_model = MyModel()
new_model.initialize_graph()
new_model.run(timesteps=100)
print(new_model)
```