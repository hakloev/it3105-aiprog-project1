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
            print(repr(todo_revise))
            if self.revise(*todo_revise):
                print("The state was revised, adding all other constraints for node %s" % todo_revise[0])
                for constraint in self.constraints[todo_revise[0].index]:
                    if constraint != todo_revise[1]: # const not eq current const
                        print("Found constraint from %s to %s" % (todo_revise[0], constraint))
                        self.queue.append((todo_revise[0], constraint))

    def revise(self, variable, constraint):
        print("Doing revise from %s to %s (%d)" % (variable, constraint.edges[0], len(self.queue)))

        revised = False

        constraint_function = constraint.get_constraint_function()

        if len(constraint.edges) >= 1:
            for node_domain_variable in self.domains[variable]:
                for constraint_domain_variable in self.domains[constraint.edges[0]]:
                    if not constraint_function(node_domain_variable, constraint_domain_variable):
                        print("Removing color %s from %s" % (node_domain_variable, self.domains[variable]))
                        self.domains[variable].remove(node_domain_variable)
                        revised = True
                        if len(self.domains[variable]) == 0:
                            print("This state is a contrabass!")
                            self.is_contradiction = True
                            break
                    else:
                        break
        return revised

    def run_again(self, variable):
        print("Running GAC again on variable %s" % variable)
        for constraint in self.constraints[variable.index]:
            print("Checking for constraint %s" % constraint)
            for j in constraint.edges:
                print("Checking for edge %s" % j)
                if variable.index != j.index:
                    self.queue.append((j, constraint))
                    print("Adding constaint from %s to %s (%d)" % (j, constraint.from_node, len(self.queue)))
        self.domain_filtering_loop()
