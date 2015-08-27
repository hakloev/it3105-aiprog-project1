from math import fabs as abs

class Board(object):

    def __init__(self, board=0):
        self.board = board
        grid_data = self.init_grid_from_file()
        self.grid = self.make_grid_from_data(grid_data)
    
    def init_grid_from_file(self):
        grid_data = list()
        with open('./boards/board%d.txt' % self.board, 'r') as f:
            for i, line in enumerate(f.readlines()):
                if i != 1:
                    grid_data.append(tuple(map(int, line.strip('()\n').split(','))))
                else:
                    grid_data.append([tuple(map(int, el.strip('()').split(','))) for el in line.rstrip().split(' ')])
        
        return grid_data

   
    @staticmethod
    def make_grid_from_data(data):
        grid_size = data[0]
        grid = [[Node(x=x, y=y) for x in range(grid_size[0])] for y in range(grid_size[1])]
        
        # Add start points to the grid
        trigger_points = data[1]
        grid[trigger_points[0][1]][trigger_points[0][0]].start = True
        grid[trigger_points[1][1]][trigger_points[1][0]].goal = True
        
        # Add obstacles to the grid
        for obstacle in data[2:]:
            for y in range(obstacle[3]):
                for x in range(obstacle[2]):
                    grid[obstacle[1] + y][obstacle[0] + x].arc_cost = float('Inf')
                    grid[obstacle[1] + y][obstacle[0] + x].char = '#'
                    grid[obstacle[1] + y][obstacle[0] + x].walkable = False
        return grid
    

    def get_all_successor_nodes(self, node):
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
            if (node.g + node.arc_cost < child.g):
                child.parent = node
                child.g = node.g + node.arc_cost
                child.f = child.g + child.h
                self.propagate_path(child)


    def heuristic(self, node):
        goal_node = self.get_goal_node()
        return abs(node.x - goal_node.x) + abs(node.y + goal_node.y) 


    def get_node(self, x, y):
        return self.grid[y][x]


    def get_start_node(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x].start:
                    return self.grid[y][x]


    def get_goal_node(self):
         for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x].goal:
                    return self.grid[y][x]
    
 
    def get_grid(self):
        return self.grid

   
    def __repr__(self):
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
        return "%s" % self.char
        #return "Node((%s, %s), s=%s, g=%s, ac=%s)" % (self.x, self.y, self.start, self.goal, self.arc_cost)


