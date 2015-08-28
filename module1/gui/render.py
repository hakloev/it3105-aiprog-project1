# -*- coding: utf8 -*-
#
# Created by 'myth' on 8/26/15

from tkinter import Canvas, BOTH, messagebox


class AbstractRenderer(object):
    """
    Abstract base class for renderer objects
    """

    def __init__(self, window):
        """
        Constructor
        :param window: Reference to the main window instance
        """
        self.window = window
        self.board = None

    def set_board(self, board):
        """
        Sets a board
        :param board: Sets an active board to the renderer object
        """

        self.board = board

    def destruct(self):
        """
        Destroys this renderer
        """

        pass

    @staticmethod
    def rgb_to_color(r, g, b):
        """
        Transforms an RGB color value to HEX
        """

        return '#%02x%02x%02x' % (r, g, b)


class CanvasRenderer(AbstractRenderer):
    """
    The CanvasRenderer can draw figures and grids on a canvas
    """

    def __init__(self, window, width=800, height=580):
        """
        Constructor
        :param window: Reference to the main window instance
        :param width: Width of the canvas
        :param height: Height of the canvas
        :return:
        """
        super().__init__(window)

        self.canvas = Canvas(self.window, width=width, height=height)
        self.canvas.pack(fill=BOTH, expand=1)

    def render(self, math_coords=False):
        """
        Renders the data
        """

        if not self.board:
            messagebox.showerror(
                'No Board',
                'No board has been selected, cannot render'
            )

        self.clear()
        payload = self.board

        start = 0
        end = len(payload)

        if math_coords:
            start = end
            end = 0

        for y in range(start, end):
            for x in range(len(payload[y])):
                coords = (
                    x * 30 + 2,
                    y * 30 + 2,
                    x * 30 + 32,
                    y * 30 + 32,
                )

                self.canvas.create_rectangle(
                    *coords,
                    fill=self.rgb_to_color(
                        x * (255 // (x + 1)),
                        y * (255 // (y + 1)),
                        100
                    )
                )

        """
        a = AStar(
            'default', # Mode to run the algortithm in. Valid inputs are [default, bfs, dfs]
            board,
            board.get_start_node(),
            board.get_goal_node()
        )
        """

    def clear(self):
        """
        Clears the content area
        """

        self.canvas.delete('all')

    def destruct(self):
        """
        Destroys this canvas
        """

        self.canvas.delete('all')
        self.canvas.destroy()
