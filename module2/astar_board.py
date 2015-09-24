__author__ = 'hakloev'

import abc
from abc import abstractmethod


class AStarBoard(metaclass=abc.ABCMeta):

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
    def heuristic(self):
        pass





