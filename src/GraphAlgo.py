import json
from typing import List
from GraphInterface import GraphInterface
from DiGraph import DiGraph
from GraphAlgoInterface import GraphAlgoInterface
from queue import PriorityQueue
import random
from matplotlib import pyplot as plt

"""A class containing functions to manipulate and present the DiGraphs data"""


class GraphAlgo(GraphAlgoInterface):
    """Initialize the GraphAlgo class with the given graph.
       @param graph: the that we will work on, if is None create a default empty graph"""

    def __init__(self, graph=None):
        if graph is None:
            self.graph = DiGraph()
        else:
            self.graph = graph

    """Return the current graph
       @return the current graph"""

    def get_graph(self) -> GraphInterface:
        return self.graph

    """Load a graph from a Json file
       @param file_name: the path to the file from the root
       @return if the loading was successful"""

    def load_from_json(self, file_name: str) -> bool:
        try:
            json_file = open(file_name, "r")
            info = json_file.read()
            flag = True
            if info.find("pos") < 0:
                flag = False
            graph_dict = json.loads(info)
            new_graph = DiGraph()
            nodes = graph_dict["Nodes"]
            for n in nodes:
                if flag:
                    str_pos = n["pos"]
                    pos = tuple(map(float, str_pos.split(',')))
                    new_graph.add_node(n["id"], pos)
                else:
                    new_graph.add_node(n["id"])
            edges = graph_dict["Edges"]
            for e in edges:
                new_graph.add_edge(e["src"], e["dest"], e["w"])
            self.graph = new_graph
            json_file.close()
            return True
        except IOError:
            return False

    """Save the graph info to a json file for later use
       @param file_name: the path to the file from the root"""

    def save_to_json(self, file_name: str) -> bool:
        try:
            json_file = open(file_name, "w")
            info = repr(self.graph)
            json_file.write(info)
            json_file.close()
            return True
        except IOError:
            return False

    """Calculate the distance and path from id1 to id2
       if there is no path return float('inf') and empty list
       utilizes the Dijkstra algorithms
       @return the path distance and a list of the nodes' ids"""

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        dist = 0
        path = list()
        nodes = self.graph.get_all_v()
        if nodes.get(id1) is not None and nodes.get(id2) is not None:
            if id1 == id2:
                path.append(id1)
                return dist, path
            self._clear_weight()
            que = list()
            src = nodes.get(id1)
            path.append(id1)
            src.set_path(path)
            que.append(src)
            while len(que) > 0:
                que.sort(key=DiGraph.Node.get_weight)
                node = que.pop(0)
                if id2 == node.get_key():
                    dist = node.get_weight()
                    path = node.get_path()
                    return dist, path
                edges = node.get_edges()
                for e in edges:
                    ni = nodes[e]
                    dist = node.get_weight() + edges[e]
                    if (dist < ni.get_weight() or ni.get_weight() == 0) and ni.get_key() != id1:
                        if dist < ni.get_weight() and ni in que:
                            que.remove(ni)
                        temp_path = node.get_path().copy()
                        temp_path.append(e)
                        ni.set_path(temp_path)
                        ni.set_weight(dist)
                        que.append(ni)
        dist = float('inf')
        path = list()
        return dist, path

    """Return a list of all the connected nodes of the given node
       utilizes the Kosaraju algorithm
       @return a list of all the connected nodes of the given node"""

    def connected_component(self, id1: int) -> list:
        nodes = self.graph.get_all_v()
        comp = list()
        if nodes.get(id1) is None:
            return comp
        self._clear_tag()
        que = list()
        que.append(nodes[id1])
        while len(que) != 0:
            node = que.pop(0)
            node.set_tag(1)
            edges = node.get_edges()
            for e in edges:
                if nodes[e].get_tag() == 0:
                    que.append(nodes[e])
        que.append(nodes[id1])
        while len(que) != 0:
            node = que.pop(0)
            node.set_tag(2)
            node.set_weight(1)
            back_edges = node.get_revers_edges()
            for e in back_edges:
                if nodes[e].get_tag() == 1:
                    que.append(nodes[e])
        for n in nodes:
            if nodes[n].get_tag() == 2:
                comp.append(n)
        return comp

    """Return a list of lists of all the connected components
       utilizes the Kosaraju algorithm
       @return a list of lists of all the connected components"""

    def connected_components(self) -> List[list]:
        nodes = self.graph.get_all_v()
        comps = list()
        if len(nodes) == 0:
            return comps
        self._clear_weight()
        for n in nodes:
            node = nodes[n]
            if node.get_weight() != 1:
                com = self.connected_component(n)
                comps.append(com)
        return comps

    """Present the graph in a GUI window, utilizes the matplotlib"""

    def plot_graph(self) -> None:
        nodes = self.graph.get_all_v()
        min_x, max_x, min_y, max_y = self._set_positions()
        if min_x == max_x:
            if min_x == 0:
                max_x = 1
            else:
                min_x *= 0.9
        if min_y == max_y:
            if min_y == 0:
                max_y = 1
            else:
                min_y *= 0.9
        r = min(max_x - min_x, max_y - min_y) / 80
        fig, ax = plt.subplots(figsize=(6, 6))
        for n in nodes:
            node = nodes[n]
            pos = node.get_pos()
            circle = plt.Circle((pos[0], pos[1]), r)
            ax.add_artist(circle)
            ax.text(pos[0], pos[1], n)
            edges = node.get_edges()
            for e in edges:
                dest = nodes[e]
                dest_pos = dest.get_pos()
                ax.annotate("", xy=(dest_pos[0], dest_pos[1]), xycoords='data',
                            xytext=(pos[0], pos[1]), textcoords='data',
                            arrowprops=dict(arrowstyle="->", connectionstyle="arc3"), )
        r *= 10
        ax.axis([min_x - r, max_x + r, min_y - r, max_y + r])
        plt.show()

    """Return the repr() of the graph"""

    def __repr__(self):
        return repr(self.graph)

    """Sets all node's weight to 0"""

    def _clear_weight(self):
        nodes = self.graph.get_all_v()
        for n in nodes:
            nodes[n].set_weight(0)

    """Set all the node's tag to 0"""

    def _clear_tag(self):
        nodes = self.graph.get_all_v()
        for n in nodes:
            nodes[n].set_tag(0)

    """Calculate the range of axis for the plot
          if the nodes lack position create a random position in the range of current nodes
          @return min_x and max_x for the x axis, min_y and max_y for the y axis"""

    def _set_positions(self):
        random.seed(5)
        nodes = self.graph.get_all_v()
        min_x = float('inf')
        min_y = float('inf')
        max_x = -float('inf')
        max_y = -float('inf')
        for n in nodes:
            node = nodes[n]
            pos = node.get_pos()
            if pos is not None:
                min_x = min(min_x, pos[0])
                min_y = min(min_y, pos[1])
                max_x = max(max_x, pos[0])
                max_y = max(max_y, pos[1])
        if min_x >= max_x:
            min_x = 0
            min_y = 0
            max_x = len(nodes)
            max_y = len(nodes)
        for n in nodes:
            node = nodes[n]
            pos = node.get_pos()
            if pos is None:
                x = random.uniform(min_x, max_x)
                y = random.uniform(min_y, max_y)
                new_pos = (x, y, 0)
                node.set_pos(new_pos)
        return min_x, max_x, min_y, max_y
