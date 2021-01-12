import unittest
import networkx as nx
from DiGraph import DiGraph
from GraphAlgo import GraphAlgo
from Networkx import Networkx


class MyTestCase(unittest.TestCase):

    def test_load(self):
        g = DiGraph()
        ga = GraphAlgo(g)
        self.assertTrue(ga.load_from_json('../data/A5'))
        g = ga.get_graph()
        self.assertEqual(g.v_size(), 48)
        self.assertEqual(g.e_size(), 166)

    def test_save(self):
        g = DiGraph()
        for i in range(10):
            g.add_node(i)
        for i in range(5):
            g.add_edge(i, i+1, i*10 + 1)
        ga1 = GraphAlgo(g)
        self.assertTrue(ga1.save_to_json('../data/test.json'))

        ga2 = GraphAlgo(DiGraph())
        ga2.load_from_json('../data/test.json')
        self.assertEqual(repr(ga1), repr(ga2))

        ga1.load_from_json('../data/G_100_800_1.json')
        self.assertTrue(ga1.save_to_json('../data/test.json'))
        ga2.load_from_json('../data/test.json')
        self.assertEqual(repr(ga1), repr(ga2))

    def test_shortest_path(self):
        g = DiGraph()
        for i in range(10):
            g.add_node(i)
        for i in range(9):
            g.add_edge(i, i+1, 1)
        g.add_edge(0, 9, 100)
        g.add_edge(0, 6, 3)
        g.add_edge(6, 8, 2)
        ga = GraphAlgo(g)
        dist, path = ga.shortest_path(0, 9)
        self.assertEqual(dist, 6)
        check = [0, 6, 8, 9]
        for i in range(len(check)):
            self.assertEqual(check[i], path[i])

        check = [7]
        dist, path = ga.shortest_path(7, 7)
        self.assertEqual(dist, 0)
        for i in range(len(check)):
            self.assertEqual(check[i], path[i])

        dist, path = ga.shortest_path(8, 5)
        self.assertEqual(dist, float('inf'))
        self.assertEqual(len(path), 0)


        nxr = Networkx()
        nxr.read('../data/G_100_800_1.json')
        nxg = nxr.get_graph()
        nx_path = nx.shortest_path(nxg, 3, 73, weight="weight")
        nx_dist = nx.shortest_path_length(nxg, 3, 73, weight="weight")

        ga = GraphAlgo()
        ga.load_from_json('../data/G_100_800_1.json')
        dist, path = ga.shortest_path(3, 73)

        self.assertEqual(dist, nx_dist)
        self.assertEqual(path, nx_path)

    def test_connected_component(self):
        g = DiGraph()
        for i in range(4):
            g.add_node(i)
        g.add_edge(1, 2, 2)
        g.add_edge(2, 1, 1)
        ga = GraphAlgo(g)

        check = [1, 2]
        comp = ga.connected_component(1)
        for i in range(len(comp)):
            self.assertEqual(check[i], comp[i])
        check = [3]
        comp = ga.connected_component(3)
        for i in range(len(comp)):
            self.assertEqual(check[i], comp[i])
        comp = ga.connected_component(5)
        self.assertEqual(len(comp), 0)

    def test_connected_components(self):
        g = DiGraph()
        for i in range(4):
            g.add_node(i)
        g.add_edge(1, 2, 2)
        g.add_edge(2, 1, 1)
        ga = GraphAlgo(g)
        check = [[0], [1, 2], [3]]
        comps = ga.connected_components()
        for c in range(len(comps)):
            com = comps[c]
            for n in range(len(com)):
                self.assertEqual(com[n], check[c][n])
        ga.load_from_json('../data/A5')
        comps = ga.connected_components()
        com = comps[0]
        for n in range(len(com)):
            self.assertEqual(com[n], n)
        nxr = Networkx()
        nxr.read('../data/G_1000_8000_1.json')
        nxg = nxr.get_graph()
        nx_comps = nx.strongly_connected_components(nxg)
        ga.load_from_json('../data/G_1000_8000_1.json')
        comps = ga.connected_components()
        comps.sort(reverse=True)
        i = 0
        for nx_comp in nx_comps:
            comp = comps[i]
            i += 1
            j = 0
            for nx_node in nx_comp:
                node = comp[j]
                j += 1
                self.assertEqual(node, nx_node)

    def test_plot(self):
        g = DiGraph()
        for i in range(10):
            g.add_node(i)
        for i in range(6):
            g.add_edge(i+1, i+2, (i+1)*10)
        ga = GraphAlgo(g)
        ga.plot_graph()
        ga.load_from_json('../data/A5')
        ga.plot_graph()
        ga.load_from_json('../data/G_100_800_0.json')
        ga.plot_graph()


if __name__ == '__main__':
    unittest.main()