# -*- coding: utf-8 -*-
from math import sqrt
from common import make_func
from common import fetch_boards_from_dir


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
        self.full_repr_mode = True

    def __lt__(self, other):
        return self.f < other.f

    def __gt__(self, other):
        return self.f > other.f

    def __repr__(self):
        if self.full_repr_mode:
            return 'Node(%d, %d, F: %d, G: %d, H: %d)' % (self.x, self.y, self.f, self.g, self.h)
        else:
            return '%d (%d, %d)' % (self.index, self.x, self.y)


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
