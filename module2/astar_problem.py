__author__ = 'hakloev'

import abc
from abc import abstractmethod


class AStarProblem(metaclass=abc.ABCMeta):
    """
    Abstract class keeping track of the minimum information A* must know of a state
    """

    @abstractmethod
    def get_start_node(self):
        pass

    @abstractmethod
    def get_goal_node(self):
        pass

    @abstractmethod
    def get_all_successor_nodes(self, node):
        pass

    @abstractmethod
    def arc_cost(self, node):
        pass

    @abstractmethod
    def heuristic(self, node):
        pass





