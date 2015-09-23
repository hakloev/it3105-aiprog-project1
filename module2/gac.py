# -*- coding: utf8 -*-
#
# Created by 'hakloev' on 9/9/15

from datastructures import *
from common import *
import inspect

colors = ['red', 'green', 'blue', 'black', 'yellow', 'purple', 'white']


class GAC(object):

    def __init__(self):
        self.variables = []
        self.domains = {}
        self.constraints = {}
        self.queue = []

    def initialize(self):
        for variable in self.variables:
            for constraint in self.constraints[variable]:
                self.queue.append((variable, constraint))

    def add_variable(self, variable, domain):
        self.variables.append(variable)
        self.domains[variable] = list(domain)
        self.constraints[variable] = []

    def add_constraint_one_way(self, x, y):
        if y not in self.constraints[x]:
            self.constraints[x].append(Constraint(x.name + ' != ' + y.name, [x, y]))

    def domain_filtering_loop(self):
        while self.queue:
            todo_revise = self.queue.pop(0)
            if self.revise(*todo_revise):
                for i in self.constraints[todo_revise[0]]:
                    if i != todo_revise[1]:
                        self.queue.append((todo_revise[0], i))

    def revise(self, variable, constraint):
        revised = False
        #print('Revise called on (%s, %s)' % (variable, constraint))
        #print('Constraints are %s' % self.constraints[variable])

        constraint_function = constraint.get_constraint_function()

        if len(constraint.edges) >= 2:
            for i in self.domains[constraint.edges[0]]:
                for j in self.domains[constraint.edges[1]]:
                    if not constraint_function(i, j):
                        self.domains[variable].remove(j)
                        if len(self.domains[variable]) == 0:
                            print("Empty domain reached, this is a dead end")
                            break
                        revised = True
                    else:
                        break  # or break?

        return revised

    def rerun(self):
        pass


if __name__ == "__main__":
    nodes = Graph.read_graph_from_file('graphs/graph01.txt')
    K = 4
    colors = colors[:K]

    g = GAC()

    for node in nodes:
        g.add_variable(node, colors)

    for node in nodes:
        for child in node.children:
            g.add_constraint_one_way(node, child)


    g.initialize()
    g.domain_filtering_loop()
