# -*- coding: utf8 -*-
#
# Created by 'myth' on 9/9/15

### THIS FILE IS USED FOR AD-HOC TESTING ONLY ###

from astar import *
from datastructures import *
from gac import *


if __name__ == '__main__':
    """
    main method
    """

    g = Graph()

    node_cache = g.read_graph_from_file('graphs/graph01.txt')

    for node_index, node in node_cache.items():
        print(('Node index %d : {} with children: {}' % node_index).format(node, node.children))
