# -*- coding: utf8 -*-
#
# Created by 'hakloev' on 9/9/15

from datastructures import *
from common import *

colors = ['red', 'green', 'blue', 'cyan', 'yellow', 'purple', 'white']


class GAC(object):

    def __init__(self, nodes=None, k=4):
        self.variables = []
        self.domains = {}
        self.constraints = {}
        self.queue = []
        self.is_contradiction = False

        global colors
        colors_to_k = colors[:k]

        for node in nodes:
            self.add_variable(node, colors_to_k)

        for node in nodes:
            for child in node.children:
                self.add_constraint_one_way(node, child)

    def initialize(self):
        for variable in self.variables:
            for constraint in self.constraints[variable.index]:
                self.queue.append((variable, constraint))

    def add_variable(self, variable, domain):
        self.variables.append(variable)
        self.domains[variable] = list(domain)
        self.constraints[variable.index] = []

    def add_constraint_one_way(self, x, y):
        if y not in self.constraints[x.index]:
            self.constraints[x.index].append(Constraint('%s != %s' % (x, y), x, [y]))

    def domain_filtering_loop(self):
        while self.queue:
            todo_revise = self.queue.pop(0)
            if self.revise(*todo_revise):
                print("I AM MODIFIED")
                for i in self.constraints[todo_revise[0].index]:
                    if i != todo_revise[1]:
                        self.queue.append((todo_revise[0], i))

    def revise(self, variable, constraint):
        revised = False

        constraint_function = constraint.get_constraint_function()

        if len(constraint.edges) >= 1:
            for i in self.domains[variable]:
                for j in self.domains[constraint.edges[0]]:
                    if variable is constraint.from_node:
                        break
                    if not constraint_function(i, j):
                        self.domains[variable].remove(j)
                        print("Removing a color: %s" % self.domains[variable])
                        if len(self.domains[variable]) == 0:
                            print("I AM A FUCKING CONTRABASS")
                            self.is_contradiction = True
                            break
                        revised = True
                    else:
                        break
        return revised

    def run_again(self, variable):
        for constraint in self.constraints[variable.index]:
            for node in constraint.edges:
                if node != variable:
                    self.queue.append((variable, constraint))
        self.domain_filtering_loop()





