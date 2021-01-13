import unittest
from Ariel_OOP_2020.Assignments.Ex3.src.DiGraph import DiGraph


class MyTestCase(unittest.TestCase):

    def test_edges(self):
        node = DiGraph.Node(0, None)

        self.assertFalse(node.add_edge(0, 100))
        self.assertTrue(node.add_edge(1, 10))
        self.assertTrue(node.add_edge(2, 20))
        self.assertTrue(node.add_revers_edge(2, 30))

        node_dict = node.get_edges()
        self.assertIsNone(node_dict.get(0))
        self.assertEqual(node_dict.get(1), 10)
        self.assertEqual(node_dict.get(2), 20)

        node_dict = node.get_revers_edges()
        self.assertEqual(node_dict.get(2), 30)

        self.assertFalse(node.remove_edge(5))
        self.assertFalse(node.remove_edge(0))
        self.assertTrue(node.remove_edge(1))

        node_dict = node.get_edges()
        self.assertIsNone(node_dict.get(5))
        self.assertIsNone(node_dict.get(0))
        self.assertIsNone(node_dict.get(1))
        self.assertEqual(node_dict.get(2), 20)

    def test_json(self):
        node1 = DiGraph.Node(1)
        node2 = DiGraph.Node(2, (1, 2, 3))
        node1.add_edge(2, 2)
        node1.add_edge(3, 1)
        node2.add_edge(4, 0)
        node2.add_edge(5, 10)
        pos = node2.get_pos()
        str_node1 = "{\"id\": %d}" % node1.get_key()
        str_node2 = "{\"pos\": \"%.16lf,%.16lf,%.16lf\", \"id\": %d}" % (pos[0], pos[1], pos[2], node2.get_key())
        self.assertEqual(repr(node1), str_node1)
        self.assertEqual(repr(node2), str_node2)





    def test_path(self):    # test path function
        node = DiGraph.Node(0)
        p = [1, 2, 3]
        node.set_path(p)
        np = node.get_path()
        for i in range(len(np)):
            self.assertEqual(p[i], np[i])
        node.set_path()
        p = list()
        np = node.get_path()
        for i in range(len(p)):
            self.assertEqual(p[i], np[i])


if __name__ == '__main__':
    unittest.main()