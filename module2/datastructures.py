# -*- coding: utf-8 -*-
from math import sqrt
from common import make_func
from common import fetch_boards_from_dir


class Board(object):
    """
    Class containing all the logic needed for setting up a board with Node objects
    Also contains the board specific functions of A*, like get_all_successor_nodes, attach_and_eval eg.
    """

    def __init__(self, mode='manhattan', board_path=None):
        """
        Initiating the Board class, with a new grid from file
        """
        self.board_path = board_path
        self.mode = mode
        self.grid = None
        self.start_node = None
        self.goal_node = None


    def get_all_successor_nodes(self, node):
        """
        Returns all adjacent nodes to the node parameter
        :param node: The node to find adjacent nodes to
        """
        nodes = []
        # Must implement for bla bla
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

    def get_node(self, x, y):
        """
        Returns a node on the given index
        :param x: X coordinate
        :param y: Y coordinate
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
        return [Graph.read_graph_from_file(fp) for fp in fetch_boards_from_dir('graphs')]

    @staticmethod
    def read_graph_from_file(file_path):
        """
        Reads input data from a file and generates a linked set of nodes
        :param file_path: Path to the file that is to be read into memory
        :return: A set of nodes
        """

        node_cache = {}

        # Read contents from specified file path
        with open(file_path) as g:
            # Retrieve the node and edge count from first line of file
            nodes, edges = map(int, g.readline().split())

            # Retrieve all node coordinates
            for node in range(nodes):
                i, x, y = map(float, g.readline().split())
                node_cache[int(i)] = Node(index=i, x=x, y=y)

            # Connect all nodes together based on edge declarations in file
            for edge in range(edges):
                from_node, to_node = map(int, g.readline().split())
                node_cache[from_node].children.add(node_cache[to_node])
                node_cache[to_node].children.add(node_cache[from_node])

        return node_cache.values()


class Node(object):

    def __init__(self, index=None, x=None, y=None):
        self.index = index
        self.name = 'n' + str(int(index))
        self.x = x
        self.y = y
        self.arc_cost = 1
        self.start = None
        self.goal = None
        self.g = 0
        self.h = 0
        self.f = 0
        self.parent = None
        self.children = set()
        self.walkable = True
        self.char = 'U'

    def __lt__(self, other):
        return self.f < other.f

    def __gt__(self, other):
        return self.f > other.f

    def __repr__(self):
        return "Node(%d, (%d, %d))" % (self.index, self.x, self.y)


class Constraint(object):

    def __init__(self, function=None, edges=None):
        self.function = function
        self.edges = edges

    def get_constraint_function(self):
        var_names = [str(n.name) for n in self.edges]
        return make_func(var_names, self.function)

    def __repr__(self):
        return "Constraint(function: %s, edges: %s" % (self.function, self.edges)

    def __str__(self):
        return "Constraint(function: %s, edges: %s" % (self.function, self.edges)
