__author__ = 'hakloev'

from astar import *
from gac import *
from astar_board import *
from copy import deepcopy


class AStarGAC(AStarBoard):

    def __init__(self, gac=None):
        gac.initialize()
        gac.domain_filtering_loop()

        self.initial_state = GACNode(gac)

    def get_start_node(self):
        return self.initial_state

    def get_goal_node(self):
        pass

    def get_all_successor_nodes(self, gac_state):
        successor_nodes = []

        for node, domain in gac_state.gac.domains.items():
            if len(domain) > 1:
                #print("GIANT DOMAIN: %s" % domain)
                for domain_element in range(len(domain)):
                    #print("DOMAIN ELEMENT IS %s" % domain_element)
                    child_state = deepcopy(gac_state)
                    child_state.gac.domains[node] = [domain[domain_element]]
                    #print("SET DOMAIN TO %s" % child_state.gac.domains[node])
                    child_state.gac.run_again(node)
                    if not child_state.gac.is_contradiction:
                        #print("Not contradiction")
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
        #print(sum((len(domain_list) - 1) for domain_list in node.gac.domains.values()))
        return sum((len(domain_list) - 1) for domain_list in node.gac.domains.values())

    # Maybe implement arc_cost here?


if __name__ == '__main__':

    nodes = Graph.read_graph_from_file('graphs/graph01.txt')

    gac_state = GAC(nodes)

    astar_gac = AStarGAC(gac=gac_state)

    solver = AStar(board=astar_gac)

    for state in solver.agenda_loop():
        print(state)

    print("Done")





