import heapq

from datastructures import *


class AStar(object):    
    """
    A A* algorithm class. Takes the mode, board, start- and goal-node

    :param mode: The mode to run the A* algorithm in
    :param board: The board containing all nodes 
    :param start_node: The instance of the start node
    :param goal_node: The instance of the end node
    """

    def __init__(self, mode='default', board=None, start_node=None, goal_node=None):
        """
        Initializing the AStar object with the given parameters 
        """
        self.mode = mode
        self.board = board
        self.start_node = start_node
        self.goal_node = goal_node

        self.open_set = []

        if self.mode == 'default':
            heapq.heapify(self.open_set)

        self.closed_set = set()

        print("# - obstacle, X - closed, O - open, @ - path")

    def agenda_loop(self):
        """
        The implementation of the A* algorithm. This is the main loop for the algorithm
        """
        self.add_node(self.start_node)
        while len(self.open_set):
            node = self.take_node()
            self.closed_set.add(node)
            node.char = 'X'

            if node == self.goal_node:
                print('--- DONE, REACHED GOAL NODE ---')
                self.print_path()
                break
            
            successors = self.board.get_all_successor_nodes(node) 
            for successor in successors:
                node.children.add(successor)
                if successor.walkable:
                    if (successor not in self.closed_set) and (successor not in self.open_set):
                        self.board.attach_and_eval(successor, node)
                        self.add_node(successor)
                        successor.char = 'O'
                    elif node.g + node.arc_cost < successor.g:
                        self.board.attach_and_eval(successor, node)
                        if successor in self.closed_set:
                            print('REACHED CLOSED NODE, PROPAGATING PATH')
                            self.board.propagate_path(node)

    def add_node(self, node):
        """
        Method to add the node to the open set depending on the mode

        :param node: The node to append to the list
        """
        return {
            'default': lambda: heapq.heappush(self.open_set, node),  # Insert to acending heap queue
            'bfs': lambda: self.open_set.append(node),  # Insert to back of queue (FIFO)
            'dfs': lambda: self.open_set.insert(0, node)  # Insert to front of queue (LIFO)
        }.get(self.mode)()

    def take_node(self):
        """
        Method to take the right node from the open set depending on the mode
        """
        return {
            'default': lambda: heapq.heappop(self.open_set),  # Get first element in queue
            'bfs': lambda: self.open_set.pop(0),
            'dfs': lambda: self.open_set.pop(0)
        }.get(self.mode)()

    def print_path(self):
        self.start_node.char = '@'
        node = self.goal_node
        while node.parent:
            node.char = "@"
            node = node.parent
        
        board = reversed(self.board.get_grid())
        for row in board:
            print(row)
