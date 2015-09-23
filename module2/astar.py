import heapq

from common import *
from astar_board import AStarBoard

class AStar(object):    
    """
    A A* algorithm class. Takes the mode, board, start- and goal-node
    :param mode: The mode to run the A* algorithm in
    :param board: The board containing all nodes 
    :param start_node: The instance of the start node
    :param goal_node: The instance of the end node
    """

    def __init__(self, mode='best', board=None):
        """
        Initializing the AStar object with the given parameters 
        """
        if not isinstance(board, AStarBoard):
            raise Exception("Board must be an instance of AStarBoard")

        self.mode = mode
        self.board = board  # initial gac_state

        self.start_node = self.board.get_start_node()
        self.goal_node = self.board.get_goal_node()

        self.open_set = []

        if self.mode == 'best':
            heapq.heapify(self.open_set)

        self.closed_set = set()

    def agenda_loop(self):
        """
        The implementation of the A* algorithm. This is the main loop for the algorithm
        """

        self.add_node(self.start_node)
        while len(self.open_set):
            node = self.take_node()
            self.closed_set.add(node)

            if node == self.goal_node:
                log('REACHED GOAL NODE')
                yield {
                    'open_set': self.open_set,
                    'closed_set': self.closed_set,
                    'path': self.get_path_from_node(node)
                }
                break

            successors = self.board.get_all_successor_nodes(node) 
            for successor in successors:
                node.children.add(successor)
                if (successor not in self.closed_set) and (successor not in self.open_set):
                    self.board.attach_and_eval(successor, node)
                    self.add_node(successor)
                elif node.g + node.arc_cost < successor.g:
                    self.board.attach_and_eval(successor, node)
                    if successor in self.closed_set:
                        debug('REACHED CLOSED NODE, PROPAGATING PATH')
                        self.board.propagate_path(node)

            # Yields the current open- and closed set to the function that called the agenda_loop
            yield {
                'open_set': self.open_set,
                'closed_set': self.closed_set,
                'path': self.get_path_from_node(node)
            }

    def attach_and_eval(self, successor, node):
        successor.parent = node
        successor.g = node.g + node.arc_cost
        successor.h = self.board.heuristic(successor)
        successor.f = successor.g + successor.h

    def propagate_path(self, node):
        for child in node.children:
            if node.g + node.arc_cost < child.g:
                child.parent = node
                child.g = node.g + node.arc_cost
                child.h = self.board.heuristic(child)
                child.f = child.g + child.h
                self.propagate_path(child)

    def add_node(self, node):
        """
        Method to add the node to the open set depending on the mode
        :param node: The node to append to the list
        """
        return {
            'best': lambda: heapq.heappush(self.open_set, node),  # Insert to acending heap queue
            'bfs': lambda: self.open_set.append(node),  # Insert to back of queue (FIFO)
            'dfs': lambda: self.open_set.insert(0, node)  # Insert to front of queue (LIFO)
        }.get(self.mode)()

    def take_node(self):
        """
        Method to take the right node from the open set depending on the mode
        """
        return {
            'best': lambda: heapq.heappop(self.open_set),  # Get first element in queue
            'bfs': lambda: self.open_set.pop(0),
            'dfs': lambda: self.open_set.pop(0)
        }.get(self.mode)()

    def backtrack_and_print_path_from_node(self, node):
        """
        This method backtracks the path from a given node, and prints the path
        It also prints the path length and total number of generated nodes
        :param node: The node to backtrack from
        """
        print('--- PATH IN REVERSE ---')
        path_length = 1  # Initiating as 1, because we do not count the goal node it self
        while node.parent:
            print(node)
            path_length += 1
            node = node.parent
        print('--- REACHED GOAL NODE (%d, %d) ---' % (path_length, (len(self.open_set) + len(self.closed_set))))

    @staticmethod
    def get_path_from_node(node):
        """
        This method returns a list containing a deepcopy of all node objects in the current path
        To be used with for instance the GUI visualisation
        :param node:
        :return:
        """
        current_path = []
        while node.parent:
            current_path.append(node)
            node = node.parent
        return current_path

    def get_path_length_from_goal_node(self):
        """
        Returns the total path length from the goal node
        :return: The length
        """
        path_length = 1  # Initiating as 1, because we do not count the goal node it self
        node = self.goal_node
        while node.parent:
            path_length += 1
            node = node.parent
        return path_length
