# -*- coding: utf8 -*-
#
# Created by 'hakloev' on 9/9/15

from common import *
from itertools import product

colors = ['red', 'green', 'blue', 'cyan', 'yellow', 'purple', 'white']


class GAC(object):

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
            # TODO: Check what is happening here

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
