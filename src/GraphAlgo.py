import json
from GraphInterface import GraphInterface
from GraphAlgoInterface import GraphAlgoInterface
from DiGraph import DiGraph
from typing import List
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
       @return if the loading was successful"""

    def load_from_json(self, file_name: str) -> bool:
        try:
            with  open(file_name, "r") as json_file:
                info = json_file.read()
                ans = True
                if info.find("pos") < 0:
                    ans = False

                new_graph = DiGraph()
                graph_dict = json.loads(info)

            nodes = graph_dict["Nodes"]
            for node in nodes:
                if ans:
                    str_pos = node["pos"]
                    pos = tuple(map(float, str_pos.split(',')))
                    new_graph.add_node(node["id"], pos)
                else:
                    new_graph.add_node(node["id"])

            edges = graph_dict["Edges"]
            for edge in edges:
                new_graph.add_edge(edge["src"], edge["dest"], edge["w"])

            self.graph = new_graph
            return True

        except IOError:
            return False

    """Save the graph info to a json file for later use
       @param file_name: the path to the file from the root"""

    def save_to_json(self, file_name: str) -> bool:
        try:
            with  open(file_name, "w") as json_file:
                info = repr(self.graph)
                json_file.write(info)
            return True

        except IOError:
            return False

    """Calculate the distance and path from id1 to id2
       if there is no path return float('inf') and empty list
       utilizes the Dijkstra algorithms
       @return the path distance and a list of the nodes' ids"""

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        nodes = self.graph.get_all_v()
        path = list()
        dist = 0

        if nodes.get(id1) is not None and nodes.get(id2) is not None:
            if id1 == id2:
                path.append(id1)
                return dist, path

            que = list()
            self._clear_weight()
            path.append(id1)
            src = nodes.get(id1)
            src.set_path(path)
            que.append(src)

            while len(que) > 0:
                que.sort(key=DiGraph.Node.get_weight)
                node = que.pop(0)
                if id2 == node.get_key():
                    path = node.get_path()
                    dist = node.get_weight()
                    return dist, path

                edges = node.get_edges()
                for edge in edges:
                    dist = node.get_weight() + edges[edge]
                    ni = nodes[edge]
                    if ni.get_key() != id1 and (ni.get_weight() == 0 or dist < ni.get_weight()):
                        if dist < ni.get_weight() and ni in que:
                            que.remove(ni)
                        temp_path = node.get_path().copy()
                        temp_path.append(edge)
                        ni.set_weight(dist)
                        ni.set_path(temp_path)
                        que.append(ni)

        path = list()
        dist = float('inf')
        return dist, path

    """Return a list of all the connected nodes of the given node
       utilizes the Kosaraju algorithm
       @return a list of all the connected nodes of the given node"""

    def connected_component(self, id1: int) -> list:
        comp = list()
        nodes = self.graph.get_all_v()

        if nodes.get(id1) is None:
            return comp
        que = list()
        que.append(nodes[id1])
        self._clear_tag()

        while len(que) != 0:
            node = que.pop(0)
            node.set_tag(1)
            edges = node.get_edges()

            for edge in edges:
                if nodes[edge].get_tag() == 0:
                    que.append(nodes[edge])
        que.append(nodes[id1])

        while len(que) != 0:
            node = que.pop(0)
            node.set_weight(1)
            node.set_tag(2)

            revers_edges = node.get_revers_edges()
            for e in revers_edges:
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
        comps = list()
        nodes = self.graph.get_all_v()

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
        max_x, max_y, min_x, min_y = self._set_positions()

        nodes = self.graph.get_all_v()

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
        fig, ax = plt.subplots(figsize=(6, 6))
        r = min(max_x - min_x, max_y - min_y) / 80

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
        nodes = self.graph.get_all_v()
        random.seed(5)
        max_x = -float('inf')
        min_x = float('inf')
        max_y = -float('inf')
        min_y = float('inf')

        for n in nodes:
            node = nodes[n]
            pos = node.get_pos()
            if pos is not None:
                max_x = max(max_x, pos[0])
                min_x = min(min_x, pos[0])
                max_y = max(max_y, pos[1])
                min_y = min(min_y, pos[1])

        if min_x >= max_x:
            max_x = len(nodes)
            min_x = 0
            max_y = len(nodes)
            min_y = 0

        for n in nodes:
            node = nodes[n]
            pos = node.get_pos()
            if pos is None:
                x = random.uniform(min_x, max_x)
                y = random.uniform(min_y, max_y)
                new_pos = (x, y, 0)
                node.set_pos(new_pos)

        return max_x, max_y, min_x, min_y
