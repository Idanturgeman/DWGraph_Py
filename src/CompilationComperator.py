import unittest
import networkx as nx
import time
from GraphAlgo import GraphAlgo
from NXJsonReader import NXJsonReader

# compares the average running time of GraphAlgo to networkx


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        nxr = NXJsonReader()
        file = '../data/G_1000_8000_1.json'
        nxr.read(file)
        self.nxg = nxr.get_graph()
        self.ga = GraphAlgo()
        self.ga.load_from_json(file)



    def test_nx_CCS(self):    # finds all the connected components 10 times and return average runtime
        start = time.time()
        for i in range(10):
            nx.strongly_connected_components(self.nxg)
        end = time.time()
        print((end - start)/10)

    def test_GA_shortest(self):   # calculate the shortest path and distance 10 times and return average runtime
        start = time.time()
        for i in range(10):
            self.ga.shortest_path(1, 25468)
        end = time.time()
        print((end - start)/10)

    def test_GA_CCS(self):     # finds all the connected components 10 times and return average runtime
        start = time.time()
        for i in range(10):
            self.ga.connected_components()
        end = time.time()
        print((end - start)/10)

    def test_GA_CC(self):      # finds the nodes that are part of 456 component 10 times and return average runtime
        start = time.time()
        for i in range(10):
            self.ga.connected_component(456)
        end = time.time()
        print((end - start)/10)


if __name__ == '__main__':
    unittest.main()