# -*- coding: utf-8 -*-
from math import sqrt


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
            self.init_grid_from_file()
        else:
            self.grid = [[]]

    def init_grid_from_file(self):
        """
        Reads and parses all the data from the text file representing the board
        """
        with open(self.board_path) as f:
            width, height = map(int, f.readline().split())
            self.grid = [[Node(x=x, y=y) for x in range(width)] for y in range(height)]
            sx, sy, gx, gy = map(int, f.readline().split())
            self.start_node = self.get_node(sx, sy)
            self.start_node.start = True
            self.goal_node = self.get_node(gx, gy)
            self.goal_node.goal = True

            for line in f.readlines():
                ox, oy, ow, oh = map(int, line.split())
                for y in range(oh):
                    for x in range(ow):
                        obstacle_node = self.get_node(ox + x, oy + y)
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
    def __init__(self, x=None, y=None):
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
        if self.f == other.f:
            return self.h < other.h
        return self.f < other.f

    def __gt__(self, other):
        if self.f == other.f:
            return self.h > other.h
        return self.f > other.f

    def __repr__(self):
        # return "%s" % self.char
        #return "Node((%s, %s), s=%s, g=%s, ac=%s)" % (self.x, self.y, self.start, self.goal, self.arc_cost)
        return "Node(%d, %d, F: %d, G: %d, H: %d)" % (self.x, self.y, self.f, self.g, self.h)
