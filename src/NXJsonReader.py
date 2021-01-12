import json
import networkx as nx

"""A utility class to load the json files to a networkx Directed graph"""


class NXJsonReader:

    """Initialize the graph that will hold the json's graph"""
    def __init__(self):
        self.graph = nx.DiGraph()

    """Return the loaded graph, make sure to load the file before using
       @return the loaded netwrokx DiGraph"""
    def get_graph(self):
        return self.graph

    """Load the json file to a networkx DiGraph
       @param file: the path to the file from the root"""
    def read(self, file):
        json_file = open(file, "r")
        info = json_file.read()
        graph_dict = json.loads(info)

        nodes = graph_dict["Nodes"]
        for node in nodes:
            self.graph.add_node(node["id"])

        edges = graph_dict["Edges"]
        for edge in edges:
            self.graph.add_edge(edge["src"], edge["dest"], weight=edge["w"])
        json_file.close()