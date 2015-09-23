# -*- coding: utf-8 -*-
from math import sqrt
from common import make_func
from common import fetch_boards_from_dir


class Board(object):
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
            grid_data = self.init_grid_from_file()
            self.make_grid_from_data(grid_data)
        else:
            self.grid = [[]]
    
    def init_grid_from_file(self):
        """
        Reads and parses all the data from the text file representing the board
        """
        grid_data = list()
        with open(self.board_path) as f:
            for i, line in enumerate(f.readlines()):
                if i != 1:
                    grid_data.append(tuple(map(int, line.strip('()\n').split(','))))
                else:
                    grid_data.append([tuple(map(int, el.strip('()').split(','))) for el in line.rstrip().split(' ')])
        
        return grid_data

    def make_grid_from_data(self, data):
        """
        Takes in a data argument and returns a populated grid
        :param data: The list representing the board
        """
        grid_size = data[0]
        self.grid = [[Node(x=x, y=y) for x in range(grid_size[0])] for y in range(grid_size[1])]
        
        # Add start points to the grid
        trigger_points = data[1]
        self.start_node = self.get_node(trigger_points[0][0], trigger_points[0][1])
        self.start_node.start = True
        self.goal_node = self.get_node(trigger_points[1][0], trigger_points[1][1])
        self.goal_node.goal = True

        # Add obstacles to the grid and set the nodes to non-walkable
        for obstacle in data[2:]:
            for y in range(obstacle[3]):
                for x in range(obstacle[2]):
                    obstacle_node = self.get_node(obstacle[0] + x, obstacle[1] + y)
                    obstacle_node.arc_cost = float('Inf')
                    obstacle_node.walkable = False

    def get_all_successor_nodes(self, node):
        """
        Returns all adjacent nodes to the node parameter
        :param node: The node to find adjacent nodes to
        """
        nodes = []
        if node.x < len(self.grid[0]) - 1: 
            nodes.append(self.get_node(node.x + 1, node.y))
        if node.y > 0:
            nodes.append(self.get_node(node.x, node.y - 1))
        if node.x > 0:
            nodes.append(self.get_node(node.x - 1, node.y))
        if node.y < len(self.grid) - 1:
            nodes.append(self.get_node(node.x, node.y + 1))
        return nodes

    def attach_and_eval(self, successor, node):
        successor.parent = node
        successor.g = node.g + node.arc_cost
        successor.h = self.heuristic(successor)
        successor.f = successor.g + successor.h

    def propagate_path(self, node):
        for child in node.children:
            if node.g + node.arc_cost < child.g:
                child.parent = node
                child.g = node.g + node.arc_cost
                child.h = self.heuristic(child)
                child.f = child.g + child.h
                self.propagate_path(child)

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
