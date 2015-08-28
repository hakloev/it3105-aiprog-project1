from math import fabs


class Board(object):
    """
    Class containing all the logic needed for setting up a board with Node objects
    Also contains the board specific functions of A*, like get_all_successor_nodes, attach_and_eval eg.
    """

    def __init__(self, board):
        """
        Initiating the Board class, with a new grid from file
        """
        self.board = board
        grid_data = self.init_grid_from_file()
        self.grid = self.make_grid_from_data(grid_data)
    
    def init_grid_from_file(self):
        """
        Reads and parses all the data from the text file representing the board
        """
        grid_data = list()
        with open(self.board) as f:
            for i, line in enumerate(f.readlines()):
                if i != 1:
                    grid_data.append(tuple(map(int, line.strip('()\n').split(','))))
                else:
                    grid_data.append([tuple(map(int, el.strip('()').split(','))) for el in line.rstrip().split(' ')])
        
        return grid_data

    @staticmethod
    def make_grid_from_data(data):
        """
        Takes in a data argument and returns a populated grid
        :param data: The list representing the board
        """
        grid_size = data[0]
        grid = [[Node(x=x, y=y) for x in range(grid_size[0])] for y in range(grid_size[1])]
        
        # Add start points to the grid
        trigger_points = data[1]
        grid[trigger_points[0][1]][trigger_points[0][0]].start = True
        grid[trigger_points[1][1]][trigger_points[1][0]].goal = True
        
        # Add obstacles to the grid and set the nodes to non-walkable
        for obstacle in data[2:]:
            for y in range(obstacle[3]):
                for x in range(obstacle[2]):
                    grid[obstacle[1] + y][obstacle[0] + x].arc_cost = float('Inf')
                    grid[obstacle[1] + y][obstacle[0] + x].char = '#'
                    grid[obstacle[1] + y][obstacle[0] + x].walkable = False
        return grid

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
                child.f = child.g + child.h
                self.propagate_path(child)

    def heuristic(self, node):
        """
        Heuristic function. Here implemented as Manhattan distance
        :param node: The node to perform the heuristic function on
        """
        goal_node = self.get_goal_node()
        return fabs(node.x - goal_node.x) + fabs(node.y + goal_node.y)

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
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x].start:
                    return self.grid[y][x]

    def get_goal_node(self):
        """
        Return the goal node for the grid
        """
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x].goal:
                    return self.grid[y][x]
 
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
        return self.f < other.f

    def __gt__(self, other):
        return self.f > other.f

    def __repr__(self):
        #return "%s" % self.char
        #return "Node((%s, %s), s=%s, g=%s, ac=%s)" % (self.x, self.y, self.start, self.goal, self.arc_cost)
        return "Node(%s, %s)" % (self.x, self.y)
