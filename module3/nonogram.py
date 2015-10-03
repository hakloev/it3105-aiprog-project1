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
            rows, cols = map(int, f.readline().split())

            self.grid = [[False]*rows]*cols
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

        # TODO: Check for contradiction or solution
        print(self.gac.csp_state.nodes)

        log('NonogramProblem initialized with %dx%d grid' % (rows, cols))

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

    def get_all_successor_nodes(self, node):
        pass

    def get_node(self, x, y):
        a = AStarState(index=0, x=x, y=y)
        a.state = self.grid[y][x]
        return a
