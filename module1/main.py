# -*- coding: utf-8 -*-

import logging

from tkinter import *

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

        self.mode = 'best'

    # Menu Commands
    def set_best_first_mode(self):
        """
        Sets the algorithm mode to best first
        """

        self.mode = 'best'

    def set_breadth_first_mode(self):
        """
        Sets the algorithm mode to breadth first
        """

        self.mode = 'bfs'

    def set_depth_first_mode(self):
        """
        Sets the algorithm mode to depth first
        """

        self.mode = 'dfs'

    @staticmethod
    def load_board(**kwargs):
        """
        Loads a specific predefined board
        """

        board = Board(kwargs['file_path'])

        print(repr(board))

        messagebox.showwarning(
            'Missing command',
            'Not implemented yet...'
        )


if __name__ == '__main__':
    """
    Application start sequence
    """

    logging.basicConfig(filename='debug.log', level=logging.DEBUG)
    log('Starting application')

    root = Tk()

    # Render the main window
    main = Main(root, Controller())
    main.set_window_size(x=1024, y=500)

    # Register menubar components
    generate_menus(main)

    # Set the initial renderer
    main.set_renderer(CanvasRenderer(main))

    # Test payload
    p = [[1 for x in range(30)] for y in range(15)]

    main.renderer.set_board(p)
    main.render()

    # Start application
    root.mainloop()
