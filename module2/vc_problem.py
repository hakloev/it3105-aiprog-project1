# -*- coding: utf8 -*-
#
# Created by 'hakloev' on 9/9/15

from copy import deepcopy

from algorithms import AStarProblem, GAC
from datastructures import AStarState, CSPState
from common import *


class VCProblem(AStarProblem):

    def __init__(self, nodes, edges):

        self.constraints = {}
        for from_node, to_node in edges:
            if from_node not in self.constraints:
                self.constraints[from_node] = []
            self.constraints[from_node].append(to_node)
            if to_node not in self.constraints:
                self.constraints[to_node] = []
            self.constraints[to_node].append(from_node)

        self.gac = GAC(csp_state=CSPState(nodes), cnet=self.constraints)

        self.gac.initialize()
        self.gac.domain_filtering_loop()

        # TODO: Check contradiction or solution

        self.initial_state = AStarState()
        self.initial_state.state = self.gac.csp_state

        self.goal_node = None

    def get_start_node(self):
        return self.initial_state

    def get_goal_node(self):
        return self.goal_node

    def get_all_successor_nodes(self, astar_state):
        """
        Fetches all successor nodes from a given CSP state
        """

        csp_state = astar_state.state
        successor_nodes = []

        for node, domains in csp_state.nodes.items():
            if len(domains) > 1:
                for d in range(len(domains)):

                    child_state = deepcopy(csp_state)
                    child_state.nodes[node] = {list(domains)[d]}

                    if DEBUG:
                        print("Domain for %s is now %s" % (node, str(child_state.nodes[node])))

                    self.gac.csp_state = child_state
                    self.gac.run_again(node)

                    if not child_state.contradiction:
                        astar_state = AStarState()
                        astar_state.state = child_state
                        successor_nodes.append(astar_state)

                return successor_nodes

    def heuristic(self, astar_state):
        """"
        From the problem description:

        A simple heuristic involves calculating the size of each domain minus one,
        then summing all those values to produce a very rough estimate of the distance
        to the goal. Devising a good, and admissible, heuristic, is more of a challenge,
        since it is very hard to estimate the extent of domain reduction incurred by any
        run of the Domain-filtering loop.
        """

        h = sum((len(domains) - 1) for domains in astar_state.state.nodes.values())
        if h == 0:
            self.goal_node = astar_state
            astar_state.is_goal = True

        if DEBUG:
            print("Heuristic for %s is %d" % (astar_state, h))

        astar_state.h = h
        return h

    def arc_cost(self, astar_state):
        return 1
