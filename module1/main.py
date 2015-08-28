# -*- coding: utf-8 -*-

import logging

from tkinter import *

from astar import AStar
from datastructures import Board
from gui.window import *
from gui.alternatives import *
from gui.render import *


class Controller(object):
    """
    Controller class exposing different option fields, menu commands etc
    """

    def __init__(self):
        """
        Constructor
        """

        self.window = None
        self.references = {}
        self.timers = []

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
        self.window.renderer.set_board(Board(kwargs['file_path']))
        self.window.render(math_coords=True)

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
            a = AStar(
                board=self.window.renderer.board,
                start_node=self.window.renderer.board.get_start_node(),
                goal_node=self.window.renderer.board.get_goal_node(),
                mode=self.references['algorithm_mode'].get()
            )

            i = 0
            for step in a.agenda_loop():
                self.timers.append(
                    self.window.parent.after(
                        i * update_interval,
                        lambda p=step['path'],
                        oss=len(step['open_set']),
                        css=len(step['closed_set']): self.window.renderer.render_path(
                            p,
                            math_coords=True,
                            open_set_size=oss,
                            closed_set_size=css
                        )
                    )
                )
                i += 1

if __name__ == '__main__':
    """
    Application start sequence
    """

    logging.basicConfig(filename='debug.log', level=logging.DEBUG)
    log('Starting application')

    root = Tk()

    # Render the main window
    main = Main(root, Controller(), name='main')
    main.controller.set_window(main)

    # Set the initial renderer
    main.set_renderer(CanvasRenderer(main.content_area))

    # Register menubar components
    generate_menus(main)

    # Set an empty board and render it
    main.renderer.set_board(Board(None))
    main.render()

    # Generate stats and options pane
    generate_options(main.options_area)
    generate_stats(main.stats_area)
    main.grid(row=0, column=0)

    # Start application
    root.mainloop()
