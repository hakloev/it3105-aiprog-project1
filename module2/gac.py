# -*- coding: utf8 -*-
#
# Created by 'myth' on 9/9/15


class GAC(object):

    def __init__(self, graph=None):
        self.graph = graph
        self.variables = []
        self.domains = {}
        self.constraints = {}

    def initialize(self):
        pass

    def domain_filtering(self):
        pass

    def rerun(self):
        pass

