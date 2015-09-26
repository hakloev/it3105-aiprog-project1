# -*- coding: utf8 -*-
#
# Created by 'hakloev' on 9/9/15

import abc
from abc import abstractmethod


class AStarProblem(metaclass=abc.ABCMeta):
    """
    Abstract class forcing implementation of the details A* need for perform the general algorithm
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





