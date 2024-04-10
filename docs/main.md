# Getting Started
Currently, **modelpy** is currently configured to work exclusively with graphical models (with a focus on bandits) using the [networkx](https://networkx.org/) package. We are working with researchers to add support for more models types across domains. To help develop this open source framework for your research domain, reach out here.

## Installation 
Make sure that you have configured your development environment to have the latest stable version of python and pip installed.
* [Pip Documentation](https://pip.pypa.io/en/stable/installation/)
* [Python Documentation](https://www.python.org/)

In your project directory, run the following command to install modelpy. 

```bash
pip add modelpy
```

## Create your model
Once you have installed modelpy, all you have to do is define your model using 3 main class functions in the **model.py** file in the root directory of your project:
1. The `__init__` function. This will define your initialization parameters. Only the parameters that are strings or numbers will be editable in the modelpy interface.
2. The `initialize_graph` function. This will define how a graph is initialized.
3. The `timestep` function. This will define the logic that your model will perform at every timestep.