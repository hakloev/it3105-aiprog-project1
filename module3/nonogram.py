# -*- coding: utf8 -*-
#
# Created by 'myth' on 10/3/15

from copy import deepcopy

from algorithms import AStarProblem, GAC
from common import *
from datastructures import AStarState, CSPState


class NonogramProblem(AStarProblem):

    def __init__(self, path):
        """
        Constructor
        """

        self.nodes = {}
        with open(path) as f:
            cols, rows = map(int, f.readline().split())

            self.grid = [[False]*cols]*rows
            self.total_rows = rows
            self.total_cols = cols

            r_reversed = []
            for row in range(rows):
                r_reversed.append(list(map(int, f.readline().split())))
            for row, counts in enumerate(reversed(r_reversed)):
                self.nodes[row] = [(row, p) for p in self.gen_patterns(counts, cols)]
            for col in range(cols):
                counts = list(map(int, f.readline().split()))
                self.nodes[rows + col] = [(col, p) for p in self.gen_patterns(counts, rows)]

        if DEBUG:
            for x in range(rows + cols):
                print(self.nodes[x])

        self.constraints = {}
        self.generate_constraints()

        def cf(a, b):
            r, domain_a = a
            c, domain_b = b
            return domain_a[c] == domain_b[r]

        self.gac = GAC(cnet=self.constraints, csp_state=CSPState(self.nodes), cf=cf)
        self.gac.initialize()
        self.gac.domain_filtering_loop()
        self.initial_state = AStarState()
        self.initial_state.state = self.gac.csp_state

        log('NonogramProblem initialized with %dx%d grid' % (rows, cols))

        # TODO: Check for contradiction or solution
        h = self.heuristic(self.initial_state)
        if h == 0:
            log("Found solution for NonogramProblem after first domain filtering loop")
            print("Found solution for NonogramProblem after first domain filtering loop")  # Should add debug flag here!


    @staticmethod
    def gen_patterns(counts, cols):
        """
        Generates pattern permutations for a given number of segments
        :param counts: A sequence of segment sizes
        :param cols: The number of columns in the matrix
        :return: A pattern matrix
        """

        if len(counts) == 0:
            row = []
            for x in range(cols):
                row.append(False)
            return [row]

        permutations = []

        for start in range(cols - counts[0] + 1):
            permutation = []
            for x in range(start):
                permutation.append(False)
            for x in range(start, start + counts[0]):
                permutation.append(True)
            x = start + counts[0]
            if x < cols:
                permutation.append(False)
                x += 1
            if x == cols and len(counts) == 0:
                permutations.append(permutation)
                break
            sub_start = x
            sub_rows = NonogramProblem.gen_patterns(counts[1:len(counts)], cols - sub_start)
            for sub_row in sub_rows:
                sub_permutation = deepcopy(permutation)
                for x in range(sub_start, cols):
                    sub_permutation.append(sub_row[x - sub_start])
                permutations.append(sub_permutation)
        return permutations

    def generate_constraints(self):
        """
        Generates constraint network
        """

        for row in range(self.total_rows):
            self.constraints[row] = [i for i in range(self.total_rows, self.total_rows + self.total_cols)]
        for col in range(self.total_cols):
            self.constraints[self.total_rows + col] = [i for i in range(0, self.total_rows)]

    def get_start_node(self):
        return self.initial_state

    def heuristic(self, astar_state):
        h = sum((len(domains) - 1) for domains in astar_state.state.nodes.values())
        if h == 0:
            astar_state.is_goal = True
        astar_state.h = h
        return h

    def arc_cost(self, node):
        return 1

    def get_goal_node(self):
        return None

    def get_all_successor_nodes(self, astar_state):
        """
        Fetches all successor nodes from a given CSP state
        In this spesific problem that means all states with a domain
        length greater than 1 for a random node
        :return: The generated successor nodes
        """
        csp_state = astar_state.state
        successor_nodes = []

        #  TODO: Unable to check if this is correct, but will see when GUI is working.
        for node, domains in csp_state.nodes.items():
            if len(domains) > 1:
                for d in range(len(domains)):
                    print(node, domains[d])
                    child_state = deepcopy(csp_state)

                    child_state.nodes[node] = [list(domains)[d]]

                    if DEBUG:
                        print("Domain for %s is now %s" % (node, str(child_state.nodes[node])))

                    self.gac.csp_state = child_state
                    self.gac.run_again(node)

                    if not child_state.contradiction:
                        astar_state = AStarState()
                        astar_state.state = child_state
                        successor_nodes.append(astar_state)

                return successor_nodes

    def get_node(self, x, y):
        a = AStarState(index=0, x=x, y=y)
        a.state = self.grid[y][x]
        return a
