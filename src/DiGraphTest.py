import unittest
from Ariel_OOP_2020.Assignments.Ex3.src.DiGraph import DiGraph


class MyTestCase(unittest.TestCase):

    def test_get_edges(self):
        graph = DiGraph()
        for i in range(6):
            graph.add_node(i)
        graph.add_edge(0, 1, 1)
        graph.add_edge(2, 1, 3)
        graph.add_edge(3, 1, 4)
        graph.add_edge(1, 2, 3)
        graph.add_edge(1, 5, 6)

        check_out = {2: 3, 5: 6}
        edges_out = graph.all_out_edges_of_node(1)
        check_in = {0: 1, 2: 3, 3: 4}
        edges_in = graph.all_in_edges_of_node(1)

        for e in edges_out:
            self.assertEqual(check_out[e], edges_out[e])
        for e in edges_in:
            self.assertEqual(check_in[e], edges_in[e])

    def test_adding(self):
        graph = DiGraph()
        for i in range(10):
            self.assertTrue(graph.add_node(i))
        for e in range(5):
            self.assertTrue(graph.add_edge(e, e+1, e*10 + 1))

        self.assertFalse(graph.add_edge(1, 1, 100))
        self.assertFalse(graph.add_edge(5, 80, 10))
        self.assertFalse(graph.add_edge(8, 5, -5))
        self.assertFalse(graph.add_edge(13, 15, 2))
        self.assertFalse(graph.add_node(5))

        self.assertEqual(graph.get_mc(), 15)
        self.assertEqual(graph.e_size(), 5)
        self.assertEqual(graph.v_size(), 10)

    def test_removing(self):
        graph = DiGraph()
        for i in range(10):
            graph.add_node(i)
        for e in range(5):
            graph.add_edge(e, e + 1, e * 10 + 1)

        self.assertFalse(graph.remove_edge(8, 9))
        self.assertFalse(graph.remove_edge(0, 100))

        self.assertTrue(graph.remove_edge(4, 5))
        self.assertEqual(graph.get_mc(), 16)
        self.assertEqual(graph.e_size(), 4)

        self.assertFalse(graph.remove_node(100))
        self.assertTrue(graph.remove_node(2))

        self.assertEqual(graph.get_mc(), 19)
        self.assertEqual(graph.e_size(), 2)
        self.assertEqual(graph.v_size(), 9)



if __name__ == '__main__':
    unittest.main()