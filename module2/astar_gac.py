__author__ = 'hakloev'

from astar import *
from gac import *
from astar_board import *


class AStarGAC(AStarBoard):

    def __init__(self, gac=None):
        gac.initialize()
        gac.domain_filtering_loop()

        self.initial_state = gac

    def get_start_node(self):
        return self.initial_state

    def get_goal_node(self):
        pass

    def get_all_successor_nodes(self, node):
        successor_nodes = []

        for node, domain in node.domains.items():
            print(node, domain)
            

    def heuristic(self):
        """"
        From the problem description:

        A simple heuristic involves calculating the size of each domain minus one,
        then summing all those values to produce a very rough estimate of the distance
        to the goal. Devising a good, and admissible, heuristic, is more of a challenge,
        since it is very hard to estimate the extent of domain reduction incurred by any
        run of the Domain-filtering loop.
        """
        pass

    # Maybe implement arc_cost here?


if __name__ == '__main__':

    nodes = Graph.read_graph_from_file('graphs/graph01.txt')

    gac_state = GAC(nodes)

    astar_gac = AStarGAC(gac=gac_state)

    solver = AStar(mode='best', board=astar_gac)

    for state in solver.agenda_loop():
        print(state)





