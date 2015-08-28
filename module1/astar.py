import heapq

from datastructures import Board
from common import *


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
                break

            successors = self.board.get_all_successor_nodes(node) 
            for successor in successors:
                node.children.add(successor)
                if successor.walkable:
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
                'closed_set': self.closed_set
            }

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

    def backtrack_path_from_node(self, node):
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


if __name__ == '__main__':
        board = Board("boards/board4.txt")
        a = AStar(
            mode='default',
            board=board,
            start_node=board.get_start_node(),
            goal_node=board.get_goal_node()
        )

        for d in a.agenda_loop():  # The agenda loop returns a generator, so we must iterate over it
            # print(d)
            continue
        a.backtrack_path_from_node(board.get_goal_node())  # Print the solution path