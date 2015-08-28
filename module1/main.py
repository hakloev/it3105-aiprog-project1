# -*- coding: utf-8 -*-

import logging

from tkinter import *

from astar import AStar
from datastructures import Board
from gui.window import *
from gui.menu import *
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
        self.mode = 'best'

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

    # Menu Commands
    def set_best_first_mode(self):
        """
        Sets the algorithm mode to best first
        """

        self.mode = 'best'
        self.solve()

    def set_breadth_first_mode(self):
        """
        Sets the algorithm mode to breadth first
        """

        self.mode = 'bfs'
        self.solve()

    def set_depth_first_mode(self):
        """
        Sets the algorithm mode to depth first
        """

        self.mode = 'dfs'
        self.solve()

    def solve(self, algorithm='astar'):
        """
        Solves the currently set board with the provided algorithm
        """

        if algorithm == 'astar':
            a = AStar(
                board=self.window.renderer.board,
                start_node=self.window.renderer.board.get_start_node(),
                goal_node=self.window.renderer.board.get_goal_node(),
                mode=self.mode
            )

            for step in a.agenda_loop():
                self.window.parent.after(500, lambda p=step['path']: self.window.renderer.render_path(p))

if __name__ == '__main__':
    """
    Application start sequence
    """

    logging.basicConfig(filename='debug.log', level=logging.DEBUG)
    log('Starting application')

    root = Tk()

    # Render the main window
    main = Main(root, Controller())
    main.controller.set_window(main)
    main.set_window_size(x=1024, y=500)

    # Register menubar components
    generate_menus(main)

    # Set the initial renderer
    main.set_renderer(CanvasRenderer(main))

    # Start application
    root.mainloop()
