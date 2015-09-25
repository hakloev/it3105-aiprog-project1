# -*- coding: utf8 -*-
#
# Created by 'hakloev' on 9/9/15

from itertools import product

from astar_gac import *
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
        print('[i] Entered domain filtering loop!')
        while self.queue:
            todo_revise = self.queue.pop()
            print(repr(todo_revise))
            if self.revise(*todo_revise):
                print("The state was revised, adding all other constraints for node %s" % todo_revise[0])
                for constraint in self.constraints[todo_revise[0].index]:
                    if constraint.edges[0] != todo_revise[1]: # const not eq current const
                        print("Found constraint from %s to %s" % (todo_revise[0], constraint))
                        self.queue.append((todo_revise[0], constraint))

    def revise(self, variable, constraint):
        print("Doing revise from %s to %s (%d)" % (variable, constraint.edges[0], len(self.queue)))

        revised = False

        constraint_function = constraint.get_constraint_function()

        to_be_removed = set()
        for arc in constraint.edges:
            if variable == arc:
                print('Variable was NOT arc!')
                for domain in self.domains[variable]:
                    print('Checking domain %s ...' % domain)
                    pairs = product([domain], self.domains[arc])
                    remove = filter(constraint_function, pairs)
                    if not remove:
                        to_be_removed.add(domain)
            else:
                print('Variable was arc!')

        if len(to_be_removed) > 0:
            revised = True
            print('Removing %s' % repr(to_be_removed))

        for d in to_be_removed:
            self.domains[variable].remove(d)

        if not self.domains[variable]:
            self.is_contradiction = True

            """
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
            """
        return revised

    def run_again(self, variable):
        print("Running GAC again on variable %s" % variable)
        for constraint in self.constraints[variable.index]:
            print("Checking for constraint %s" % constraint)
            for j in constraint.edges:
                print("Checking for edge %s" % j)
                if variable.index != j.index:
                    self.queue.append((j, constraint))
                    print("Adding constaint from %s to %s (%d)" % (j, constraint.edges[0], len(self.queue)))
        self.domain_filtering_loop()


class GAC2Optimized(object):

    def __init__(self, nodes, edges, cf=lambda x, y: x != y):
        self.nodes = nodes
        self.contradiction = False
        self.constraints = {}
        self.constraint_function = cf
        self.queue = []

        for from_node, to_node in edges:
            if from_node not in self.constraints:
                self.constraints[from_node] = []
            self.constraints[from_node].append(to_node)
            if to_node not in self.constraints:
                self.constraints[to_node] = []
            self.constraints[to_node].append(from_node)

    def initialize(self):
        """
        Initializes the queue with all constraint permutations
        :return:
        """

        for node, edges in self.constraints.items():
            self.queue.extend((node, edge) for edge in edges)

        log('Queue initialized with %d pairs' % len(self.queue))

    def revise(self, from_node):
        to_be_removed = []
        for arc in self.constraints[from_node]:
            for domain in self.nodes[from_node]:
                remove = True
                for x, y in product([domain], self.nodes[arc]):
                    if self.constraint_function(x, y):
                        remove = False
                        break

                if remove:
                    if DEBUG:
                        print('Removing domain %s from %s' % (COLORMAP[domain], from_node))
                    to_be_removed.append(domain)

        try:
            for domain in to_be_removed:
                self.nodes[from_node].remove(domain)
        except KeyError:
            pass
            # TODO: Check wtf is going on here

        if to_be_removed:
            if not self.nodes[from_node]:
                self.contradiction = True
                if DEBUG:
                    print('Contradiction')
            return True

        return False

    def domain_filtering_loop(self):
        while self.queue:
            from_node, to_node = self.queue.pop(0)
            if self.revise(from_node):
                for arc in self.constraints[from_node]:
                    if arc != from_node:
                        self.queue.append((arc, from_node))

    def run_again(self, node):
        for arc in self.constraints[node]:
            if node != arc:
                self.queue.append((arc, node))
        self.domain_filtering_loop()
