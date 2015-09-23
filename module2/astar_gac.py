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
        pass

    def get_goal_node(self):
        pass

    def get_all_successor_nodes(self, node):
        pass

    def heuristic(self):
        pass


if __name__ == '__main__':

    nodes = Graph.read_graph_from_file('graphs/graph01.txt')

    gac_state = GAC(nodes)

    astar_gac = AStarGAC(gac=gac_state)

    solver = AStar(board=astar_gac)

    solver.agenda_loop()





