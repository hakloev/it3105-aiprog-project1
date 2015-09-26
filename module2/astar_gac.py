# -*- coding: utf8 -*-
#
# Created by 'hakloev' on 9/9/15


from datastructures import *
from astar_problem import *
from copy import deepcopy
from common import *


class AStarGAC(AStarProblem):

    def __init__(self, gac=None):
        gac.initialize()
        gac.domain_filtering_loop()

        self.initial_state = GACNode(gac)
        self.goal_node = None

    def get_start_node(self):
        return self.initial_state

    def get_goal_node(self):
        return self.goal_node

    def get_all_successor_nodes(self, gac_state):
        successor_nodes = []
        for node, domain in gac_state.gac.nodes.items():
            if len(domain) > 1:
                if DEBUG:
                    print("New GACState created")
                for domain_element in range(len(domain)):
                    child_state = deepcopy(gac_state)
                    child_state.index += 1
                    child_state.gac.nodes[node] = {list(domain)[domain_element]}
                    if DEBUG:
                        print("Domain for %s is now %s" % (node, child_state.gac.nodes[node]))
                    child_state.gac.run_again(node)
                    if not child_state.gac.contradiction:
                        successor_nodes.append(child_state)
                return successor_nodes

    def heuristic(self, node):
        """"
        From the problem description:

        A simple heuristic involves calculating the size of each domain minus one,
        then summing all those values to produce a very rough estimate of the distance
        to the goal. Devising a good, and admissible, heuristic, is more of a challenge,
        since it is very hard to estimate the extent of domain reduction incurred by any
        run of the Domain-filtering loop.
        """

        h = sum((len(domains) - 1) for domains in node.gac.nodes.values())
        if h == 0:
            self.goal_node = self
        if DEBUG:
            print("Heuristic for %s is %d" % (node, h))

        return h

    def arc_cost(self, node):
        return 1
