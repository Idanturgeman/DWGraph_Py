import unittest
import networkx as nx
import time
from GraphAlgo import GraphAlgo

import json

"""A utility class to load the json files to a networkx Directed graph"""


class Networkx:

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



class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        nxr = Networkx()
        file = '../data/G_1000_8000_1.json'
        nxr.read(file)
        self.nxg = nxr.get_graph()
        self.ga = GraphAlgo()
        self.ga.load_from_json(file)



    def test_nx_CCS(self):
        start = time.time()
        for i in range(10):
            nx.strongly_connected_components(self.nxg)
        end = time.time()
        print((end - start)/10)

    def test_GA_shortest(self):
        start = time.time()
        for i in range(10):
            self.ga.shortest_path(1, 25468)
        end = time.time()
        print((end - start)/10)

    def test_GA_CCS(self):
        start = time.time()
        for i in range(10):
            self.ga.connected_components()
        end = time.time()
        print((end - start)/10)

    def test_GA_CC(self):
        start = time.time()
        for i in range(10):
            self.ga.connected_component(456)
        end = time.time()
        print((end - start)/10)


if __name__ == '__main__':
    unittest.main()