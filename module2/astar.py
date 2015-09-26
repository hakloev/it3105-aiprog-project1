# -*- coding: utf8 -*-
#
# Created by 'hakloev' on 9/9/15

import heapq

from common import *
from astar_problem import AStarProblem


class AStar(object):    
    """
    A general A* algorithm class. Takes the mode and a problem instance as parameters
    :param mode: The mode to run the A* algorithm in
    :param problem: The problem to run A* on
    """

    def __init__(self, mode='best', problem=None):
        """
        Initializing the A* object with the given parameters
        """
        if not isinstance(problem, AStarProblem):
            raise Exception("Problem must be an instance of AStarProblem")

        self.mode = mode
        self.problem = problem

        self.open_set = []
        self.closed_set = set()

        self.start_node = self.problem.get_start_node()
        self.goal_node = None

        self.path = []
        self.parent_of = {}

        if self.mode == 'best':
            heapq.heapify(self.open_set)

        print('A* initiated with valid problem instance')

    def agenda_loop(self):
        """
        The implementation of the A* algorithm. This is the main loop for the algorithm
        """

        self.problem.heuristic(self.start_node)
        self.add_node((self.start_node.h, self.start_node))

        while len(self.open_set):
            node = self.take_node()
            self.closed_set.add(node)

            if self.problem.heuristic(node) == 0:
                if DEBUG:
                    print('Reached goal node!')
                log('Reached the goal node for this problem instance')
                yield {
                    'open_set': self.open_set,
                    'closed_set': self.closed_set,
                    'path': self.get_path_from_node([node])
                }
                break

            successors = self.problem.get_all_successor_nodes(node)

            for successor in successors:
                node.children.add(successor)
                if (successor not in self.closed_set) and (successor not in self.open_set):
                    self.attach_and_eval(successor, node)
                    self.add_node((successor.f, successor))
                elif node.g + self.problem.arc_cost(node) < successor.g:
                    self.attach_and_eval(successor, node)  # Returns f value, but is never used
                    if successor in self.closed_set:
                        debug('Reached closed node, propagating path')
                        self.propagate_path(node)

            # Yields the current open- and closed set to the function that called the agenda_loop
            yield {
                'open_set': self.open_set,
                'closed_set': self.closed_set,
                'path': self.get_path_from_node([node])
            }

    def attach_and_eval(self, successor, node):
        self.parent_of[successor] = node
        successor.g = node.g + self.problem.arc_cost(node)
        successor.h = self.problem.heuristic(successor)
        successor.f = successor.g + self.problem.heuristic(successor)

    def propagate_path(self, node):
        for child in node.children:
            if node.g + self.problem.arc_cost(node) < child.g:
                self.parent_of[child] = node
                child.g = node.g + self.problem.arc_cost[node]
                child.h = self.problem.heuristic(child)
                child.f = child.g + child.h
                self.propagate_path(child)

    def add_node(self, node):
        """
        Method to add the node to the open set depending on the mode
        :param node: The node to append to the list
        """
        return {
            'best': lambda: heapq.heappush(self.open_set, node),  # Insert to ascending heap queue
            'bfs': lambda: self.open_set.append(node),  # Insert to back of queue (FIFO)
            'dfs': lambda: self.open_set.insert(0, node)  # Insert to front of queue (LIFO)
        }.get(self.mode)()

    def take_node(self):
        """
        Method to take the right node from the open set depending on the mode
        """
        return {
            'best': lambda: heapq.heappop(self.open_set)[1],  # Get first element in queue
            'bfs': lambda: self.open_set.pop(0),
            'dfs': lambda: self.open_set.pop(0)
        }.get(self.mode)()

    def get_path_from_node(self, path):
        """
        This method returns a list containing a deepcopy of all node objects in the current path
        To be used with for instance the GUI visualisation
        :param node:
        :return:
        """
        while path[-1] != self.problem.get_start_node():
            path.append(self.parent_of[path[-1]])
        return path[::1]


