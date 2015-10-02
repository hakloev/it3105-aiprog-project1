# -*- coding: utf-8 -*-

from math import sqrt

from algorithms import AStarProblem
from common import *


class Node(object):
    """
    Basic Node object that keeps the foundational properties of a Node
    that might be used in some sort of state or graph representation
    """

    def __init__(self, index=None, x=None, y=None):
        """
        Constructor
        """

        self.index = index
        self.x = x
        self.y = y
        self.parent = None
        self.children = set()

    def __str__(self):
        return 'N' + str(self.index)

    def __repr__(self):
        """
        String representation of the BasicNode object
        """

        return 'Node %d (%d, %d)' % (self.index, self.x, self.y)


class Board(AStarProblem):
    """
    Class containing all the logic needed for setting up a board with Node objects
    Also contains the board specific functions of A*, like get_all_successor_nodes, attach_and_eval eg.
    """

    def __init__(self, board_path, mode='manhattan'):
        """
        Initiating the Board class, with a new grid from file
        """

        self.board_path = board_path
        self.mode = mode
        self.grid = None
        self.start_node = None
        self.goal_node = None

        if board_path:
            self.init_grid_from_file()
        else:
            self.grid = [[]]

    def init_grid_from_file(self):
        """
        Reads and parses all the data from the text file representing the board
        """
        with open(self.board_path) as f:
            width, height = map(int, f.readline().split())
            self.grid = [[AStarState(index=(y*x+x), x=x, y=y) for x in range(width)] for y in range(height)]
            sx, sy, gx, gy = map(int, f.readline().split())
            self.start_node = self.get_node(sx, sy)
            self.start_node.is_start = True
            self.goal_node = self.get_node(gx, gy)
            self.goal_node.is_goal = True

            for line in f.readlines():
                ox, oy, ow, oh = map(int, line.split())
                for y in range(oh):
                    for x in range(ow):
                        obstacle_node = self.get_node(ox + x, oy + y)
                        obstacle_node.walkable = False

    def get_all_successor_nodes(self, node):
        """
        Returns all adjacent nodes to the node parameter
        :param node: The node to find adjacent nodes to
        """
        nodes = []
        if node.x < len(self.grid[0]) - 1 and self.get_node(node.x + 1, node.y).walkable:
            nodes.append(self.get_node(node.x + 1, node.y))
        if node.y > 0 and self.get_node(node.x, node.y - 1).walkable:
            nodes.append(self.get_node(node.x, node.y - 1))
        if node.x > 0 and self.get_node(node.x - 1, node.y).walkable:
            nodes.append(self.get_node(node.x - 1, node.y))
        if node.y < len(self.grid) - 1 and self.get_node(node.x, node.y + 1).walkable:
            nodes.append(self.get_node(node.x, node.y + 1))

        return nodes

    def heuristic(self, node):
        """
        Heuristic function. Here implemented as Manhattan distance
        :param node: The node to perform the heuristic function on
        """

        return {
            'manhattan': lambda: abs(node.x - self.goal_node.x) + abs(node.y - self.goal_node.y),
            'euclidean': lambda: sqrt(pow((node.x - self.goal_node.x), 2) + pow((node.y - self.goal_node.y), 2))
        }.get(self.mode)()

    def arc_cost(self, node):
        """
        Fetches the arc cost of the given node
        :param node: AStarNode instance
        :return: Values ranging from 1 to Inf
        """
        return node.arc_cost

    def get_node(self, x, y):
        """
        Returns a node on the given index
        :param x: X coordinate
        :param y: Y coordinate
        :return: AStarNode instance
        """
        return self.grid[y][x]

    def get_start_node(self):
        """
        Return the start node for the grid
        """
        return self.start_node

    def get_goal_node(self):
        """
        Return the goal node for the grid
        """
        return self.goal_node

    def get_grid(self):
        """
        Returns the grid itself
        """
        return self.grid

    def __repr__(self):
        """
        Returns a string representation of the board/grid
        """
        string = ""
        for row in reversed(self.grid):
            string += "%s\n" % repr(row)
        return string


class Graph(object):
    """
    Jazzing the graph since 1985
    """

    @staticmethod
    def read_all_graphs():
        return [Graph.read_graph_from_file(fp) for fp in fetch_files_from_dir()]

    @staticmethod
    def read_graph_from_file(file_path, networkx_graph=None, lightweight=False):
        """
        Reads input data from a file and generates a linked set of nodes
        :param file_path: Path to the file that is to be read into memory
        :return: A set of nodes
        """

        node_cache = {}
        edge_set = []

        # Read contents from specified file path
        with open(file_path) as g:
            # Retrieve the node and edge count from first line of file
            nodes, edges = map(int, g.readline().split())
            if networkx_graph:
                debug('NetworkX Graph instance provided, adding nodes directly to graph.')

            # Retrieve all node coordinates
            for node in range(nodes):
                i, x, y = map(float, g.readline().split())
                n = Node(index=int(i), x=x, y=y)
                node_cache[int(i)] = n

                # Add the node to the networkx graph
                if networkx_graph is not None:
                    networkx_graph.add_node(n)

            # Connect all nodes together based on edge declarations in file
            for edge in range(edges):
                from_node, to_node = map(int, g.readline().split())
                node_cache[from_node].children.add(node_cache[to_node])
                node_cache[to_node].children.add(node_cache[from_node])

                # This is nice to have
                edge_set.append((from_node, to_node))

                # Add the edge in the networkx graph
                if networkx_graph is not None:
                    networkx_graph.add_edge(node_cache[from_node], node_cache[to_node])

        if lightweight:
            return [n.index for n in node_cache.values()], edge_set
        else:
            return node_cache.values(), edge_set


class CSPState(object):
    """
    This class represent a state in a GAC problem, and contains
    only the current domain sets for all the nodes in the problem.

    A contradiction flag can be set during iteration
    """

    def __init__(self, nodes={}):
        """
        Constructor, takes in dict mapping from node to domain set
        """

        self.nodes = nodes
        self.contradiction = False


class AStarState(Node):
    """
    The AstarNode is a specialization of a Node, that in addition keeps track of arc-cost, start and goal flags,
    as well as F, G and H values.
    """

    def __init__(self, index=None, x=None, y=None):
        super(AStarState, self).__init__(index=index, x=x, y=y)
        self.is_start = None
        self.is_goal = None
        self.state = None
        self.arc_cost = 1
        self.g = 0
        self.h = 0
        self.f = 0
        self.walkable = True
        self.full_repr_mode = True

    def __lt__(self, other):
        if self.f == other.f:
            return self.h < other.h
        return self.f < other.f

    def __gt__(self, other):
        if self.f == other.f:
            return self.h > other.h
        return self.f > other.f

    def __repr__(self):
        if self.full_repr_mode:
            return 'A*Node(%d, %d, F: %d, G: %d, H: %d)' % (self.x, self.y, self.f, self.g, self.h)
        else:
            return 'A*Node(%d (%d, %d))' % (self.index, self.x, self.y)
