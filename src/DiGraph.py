import json
from GraphInterface import GraphInterface

""" an implementation of abstract class GraphInterface.
    implementing data structure of directed weighted graph"""


class DiGraph(GraphInterface):
    """A nested Node class, implements the node structure in the graph"""

    class Node:

        """Create a node with its unique id"""

        def __init__(self, key, pos=None):
            self.key = key
            self.tag = 0
            self.weight = 0
            self.edges = dict()
            self.pos = pos
            self.revers_edges = dict()
            self.path = list()

        """Returns a dictionary of all the edges exiting the node {dest id<int>: edge weight<float>}
                  @returns a dictionary of all the edges exiting the node {dest id<int>: edge weight<float>}"""

        def get_edges(self):
            return self.edges

        """Connect this node to another with an edge,
           this node is the source of the edge
           @return if the connection was successful"""

        def add_edge(self, key, weight):
            if key != self.key and self.edges.get(key) is None:
                self.edges.update([(key, weight)])
                return True
            return False

        """Remove an edge that start in this node
           @return if the removal was successful"""

        def remove_edge(self, key):
            if self.edges.get(key) is not None:
                self.edges.pop(key)
                return True
            return False

        """Connect this node to another with an edge
           @return if the connection was successful"""

        def add_revers_edge(self, key, weight):
            if key != self.key and self.revers_edges.get(key) is None:
                self.revers_edges.update([(key, weight)])
                return True
            return False

        """Remove an edge that end in this node
           @return if the removal was successful"""

        def remove_revers_edge(self, key):
            if self.revers_edges.get(key) is not None:
                self.revers_edges.pop(key)
                return True
            return False

        """Returns a dictionary of all the edges entering the node {src id<int>: edge weight<float>}
           @returns a dictionary of all the edges entering the node {src id<int>: edge weight<float>}"""

        def get_revers_edges(self):
            return self.revers_edges

        """Return a list containing the ids of nodes, mainly for algorithmic purposes
           @:return a list containing the ids of nodes"""

        def get_path(self):
            return self.path

        """Sets a new path list to the node, mainly for algorithmic purposes
           @param path: the new list, if is empty resets the path"""

        def set_path(self, path=None):
            if path is None:
                self.path = list()
            else:
                self.path = path

        """Appends the path list with the new key
           @param key: the key of the new node"""

        def append_path(self, key):
            self.path.append(key)

#################################Getters_and_Setters###########################################################


        def get_key(self):
            return self.key

        def get_weight(self):
            return self.weight

        def set_weight(self, weight):
            self.weight = weight

        def get_tag(self):
            return self.tag

        def set_tag(self, tag):
            self.tag = tag

        def get_pos(self):
            return self.pos

        def set_pos(self, pos):
            self.pos = pos

        """Return a list containing dictionaries of edges
           @return a list containing dictionaries of edges"""

        def get_edge_list(self):
            edge_list = []
            for e in self.edges:
                edge_dict = {"src": self.key, "w": self.edges[e], "dest": e}
                edge_list.append(edge_dict)
            return edge_list

        """Return a string containing the node's information in a json format
           @return a string containing the node's information in a json format"""

        def __repr__(self):
            info = json.dumps(self.get_node())
            return info

        """Returns a dictionary of the node's data
                  {pos:x,y,z, id:key} or if there is no pos {id:key}
                  @return a dictionary of the node's data"""

        def get_node(self):
            if self.pos is None:
                node_dict = {"id": self.key}
            else:
                str_pos = "%.16lf,%.16lf,%.16lf" % (self.pos[0], self.pos[1], self.pos[2])
                node_dict = {"pos": str_pos, "id": self.key}
            return node_dict

    ################### DiGraph_Class ###############################################################################

    """create an empty graph"""

    def __init__(self):
        self.mc = 0
        self.ec = 0
        self.nodes = dict()

    def e_size(self) -> int:
        return self.ec

    def v_size(self):
        return len(self.nodes)

    def get_all_v(self) -> dict:
        return self.nodes

    """Returns a dictionary of all the edges exiting the node {dest id<int>: edge weight<float>}
       @returns a dictionary of all the edges exiting the node {dest id<int>: edge weight<float>}"""

    def all_out_edges_of_node(self, id1: int) -> dict:
        if self.nodes.get(id1) is not None:
            return self.nodes.get(id1).get_edges()

    """Returns a dictionary of all the edges entering the node {src id<int>: edge weight<float>}
                  @returns a dictionary of all the edges entering the node {src id<int>: edge weight<float>}"""

    def all_in_edges_of_node(self, id1: int) -> dict:
        if self.nodes.get(id1) is not None:
            return self.nodes.get(id1).get_revers_edges()

    def get_mc(self) -> int:
        return self.mc

    """Add a new node to the graph, if the node already exist does nothing.
       @return if the addition was successful"""

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        if self.nodes.get(node_id) is None:
            node = self.Node(node_id, pos)
            self.nodes.update([(node_id, node)])
            self.mc += 1
            return True
        return False

    """connects 2 nodes with an edge weighted as weight,
          when id1 is the src node and id2 is the dest
          @return if the addition was successful"""

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        if id1 == id2 or weight <= 0:
            return False
        if self.nodes.get(id1) is not None and self.nodes.get(id2) is not None:
            src = self.nodes.get(id1)
            dest = self.nodes.get(id2)

            if src.add_edge(id2, weight) and dest.add_revers_edge(id1, weight):
                self.ec += 1
                self.mc += 1
                return True
        return False

    """Remove an existing edge from the graph
       @return if the removal was successful"""

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        if node_id1 == node_id2:
            return False
        if self.nodes.get(node_id1) is not None and self.nodes.get(node_id2) is not None:
            src = self.nodes.get(node_id1)
            dest = self.nodes.get(node_id2)
            if src.remove_edge(node_id2) and dest.remove_revers_edge(node_id1):
                self.ec -= 1
                self.mc += 1
                return True
        return False

    """Remove the node from the graph and all his edges,
          if the node doesn't exist, does nothing
          @return if the removal was successful"""

    def remove_node(self, node_id: int) -> bool:
        if self.nodes.get(node_id) is not None:
            node = self.nodes.get(node_id)
            edges = node.get_edges()
            back_edges = node.get_revers_edges()
            self.ec -= (len(edges) + len(back_edges))
            self.mc += (len(edges) + len(back_edges) + 1)

            for n in edges:
                self.nodes.get(n).remove_revers_edge(node_id)
            for n in back_edges:
                self.nodes.get(n).remove_edge(node_id)
            self.nodes.pop(node_id)
            return True
        return False

    def __repr__(self):
        info = json.dumps(self.get_graph())
        return info

    """Returns a dictionary containing all the edges and nodes of the graph
       @return a dictionary containing all the edges and nodes of the graph
       {Edges:[edge1, edge2 ...], Nodes:[node1, node2, ...]}"""

    def get_graph(self):
        node_list = []
        edge_list = []
        for n in self.nodes:
            node = self.nodes[n].get_node()
            node_list.append(node)
            edges = self.nodes[n].get_edge_list()
            edge_list.extend(edges)
        graph_dict = {"Edges": edge_list, "Nodes": node_list}
        return graph_dict
