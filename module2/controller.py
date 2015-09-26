# -*- coding: utf8 -*-
#
# Created by 'myth' on 9/23/15

import random

from tkinter import messagebox
from tkinter import *

from datastructures import Graph, Node
from gui.alternatives import *
from gui.render import GraphRenderer
from gui.window import Main
from astar import *
from vc_problem import *
from gac import *
import time

GUI_UPDATE_INTERVAL = 50
TIMEOUT_THRESHOLD = 60


class MainController(object):
    """
    Controller class controlling window components
    """

    def __init__(self):
        self.window = None
        self.references = {}
        self.timers = []
        self.graph = None

    def clear_timers(self):
        """
        Clears all registered timers from the event loop
        """

        for timer in self.timers:
            self.window.parent.after_cancel(timer)
        self.timers = []

    def clear_stats(self):
        """
        Resets stats counters frame
        """

        if 'path_length' in self.references:
            self.references['path_length'].set('Path length: 0')
        if 'open_set_size' in self.references:
            self.references['open_set_size'].set('OpenSet size: 0')
        if 'closed_set_size' in self.references:
            self.references['closed_set_size'].set('ClosedSet size: 0')

    def set_window(self, window):
        """
        Sets a reference to the main tkinter window
        """

        self.window = window

    def load_board(self, **kwargs):
        """
        Loads a specific predefined board
        """

        if 'file_path' not in kwargs:
            messagebox.showerror(
                'Missing file path',
                'No file path was provided!'
            )

        self.window.renderer.clear()
        # Load the graph from file, and provide networkx graph instance for rendering
        Graph.read_graph_from_file(kwargs['file_path'], networkx_graph=self.window.renderer.graph)

        self.window.renderer.render_graph()

    def solve(self, algorithm='astar'):
        """
        Solves the currently set board with the provided algorithm
        """

        # Clear any active rendering timers
        self.clear_timers()

        update_interval = GUI_UPDATE_INTERVAL
        if 'update_interval' in self.references:
            try:
                update_interval = self.references['update_interval'].get()
                update_interval = int(update_interval)
            except ValueError:
                messagebox.showerror(
                    'Invalid update interval',
                    'Update interval must be in milliseconds'
                )

        if algorithm == 'astar':
            if 'heuristic' in self.references:
                self.window.renderer.board.mode = self.references['heuristic'].get()
            a = AStar(
                board=self.window.renderer.board,
                mode=self.references['algorithm_mode'].get()
            )

            i = 0
            for step in a.agenda_loop():
                self.timers.append(
                    self.window.parent.after(
                        i * update_interval,
                        lambda path=step['path'],
                        o=len(step['open_set']),
                        c=len(step['closed_set']): self.window.renderer.render_path(
                            path,
                            math_coords=True,
                            open_set_size=o,
                            closed_set_size=c
                        )
                    )
                )
                i += 1

        if algorithm == 'astar_gac':

            g = self.window.renderer.graph
            n = g.nodes()
            e = [(x.index, y.index) for x, y in g.edges()]

            k = int(self.references['k_value'].get())
            n = {node.index: set([i for i in range(k)]) for node in n}
            gac_state = GAC(n, e)

            def arc_constraint(x, y):
                return x != y

            gac_state.constraint_function = arc_constraint
            vc_problem = VCProblem(gac=gac_state)
            solver = AStar(problem=vc_problem)

            t = time.time()

            i = 0
            for step in solver.agenda_loop():
                print('Step %d' % i)
                p = step['path']
                oss = len(step['open_set'])
                css = len(step['closed_set'])
                self.window.renderer.render_path(
                    p=p,
                    open_set_size=oss,
                    closed_set_size=css
                )

                i += 1
                if time.time() - t > TIMEOUT_THRESHOLD or i > 600:
                    messagebox.showerror(
                        'Timeout!',
                        'Took too much time: %d steps in %f seconds...' % (i, time.time() - t)
                    )
                    break

            messagebox.showinfo(
                'Complete!',
                'Found a solution in %f seconds...' % (time.time() - t)
            )

    def debug(self):
        """
        Performs a debug print to the console for interactive debugging
        """
        g = self.window.renderer.graph
        print(g.nodes())
        print(g.edges())

    def add_random_node(self):
        """
        DEBUG
        :return:
        """
        g = self.window.renderer.graph
        n = Node(index=random.randint(1337, 13337), x=random.randint(0, 40), y=random.randint(0, 40))
        g.add_node(n)
        g.add_edge(n, g.nodes()[0])
        g.add_edge(n, g.nodes()[2])

        print(g.nodes())

        # Replace draw_only with a tuple containing a nodeset and edgeset to only draw those
        self.window.renderer.render_graph(nodelist=[n], edgelist=[(n, g.nodes()[0]), (n, g.nodes()[2])])

    def exit(self):
        """
        Destroys the window
        :return:
        """

        self.window.parent.quit()
