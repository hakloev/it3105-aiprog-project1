# -*- coding: utf8 -*-
#
# Created by 'myth' on 8/26/15

from tkinter import Canvas, BOTH, messagebox

from common import debug

GUI_UPDATE_INTERVAL = 50  # ms
BOARD_CELL_SIZE = 10  # pixels


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
        self.board_height = 0

    def set_board(self, board):
        """
        Sets a board
        :param board: Sets an active board to the renderer object
        """

        self.board = board
        self.board_height = len(self.board.grid)

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

    def __init__(self, window, width=600, height=580):
        """
        Constructor
        :param window: Reference to the main window instance
        :param width: Width of the canvas
        :param height: Height of the canvas
        :return:
        """
        super().__init__(window)

        self.canvas = Canvas(self.window, width=width, height=height)
        self.canvas.grid(row=0, column=0, sticky='NE', padx=BOARD_CELL_SIZE)
        self.path_sprites = set()

    def render_board(self, math_coords=False):
        """
        Renders the data
        """

        debug('CanvasRenderer.render_board() called')

        if not self.board:
            messagebox.showerror(
                'No Board',
                'No board has been selected, cannot render'
            )

        self.clear()
        payload = self.board.grid

        row_range = range(0, self.board_height)
        # If we are drawing using mathematical coordinates (Y-axis reversed)
        if math_coords:
            row_range = range(self.board_height - 1, -1, -1)

        # Iterate through all nodes, create sprite coords and determine fill color
        for y in row_range:
            for x in range(len(payload[y])):

                draw_y = y
                if math_coords:
                    draw_y = self.board_height - y

                coords = (
                    x * BOARD_CELL_SIZE + 1,
                    draw_y * BOARD_CELL_SIZE + 1,
                    x * BOARD_CELL_SIZE + BOARD_CELL_SIZE + 1,
                    draw_y * BOARD_CELL_SIZE + BOARD_CELL_SIZE + 1,
                )

                node = self.board.get_node(x, y)
                fill_color = '#FFFFFF'
                if not node.walkable:
                    fill_color = '#000000'
                elif node.start:
                    fill_color = '#4040FF'
                elif node.goal:
                    fill_color = '#40FF40'

                self.canvas.create_rectangle(
                    *coords,
                    fill=fill_color
                )

    def render_path(self, path, math_coords=False, **kwargs):
        """
        Renders path nodes on top of the map, after clearing previously rendered path nodes
        :param path: A list of Node objects
        """

        open_set = kwargs['open_set_size']
        closed_set = kwargs['closed_set_size']

        # Remove all previously rendered path sprites from canvas
        for sprite in self.path_sprites:
            self.canvas.delete(sprite)

        self.path_sprites.clear()

        # Add sprites for current path
        for node in reversed(path):
            # If we are drawing using mathematical coordinates (y-reversed)
            y = node.y
            if math_coords:
                y = self.board_height - node.y

            # Create the coordinates and dimension tuple
            coords = (
                node.x * BOARD_CELL_SIZE + 1,
                y * BOARD_CELL_SIZE + 1,
                node.x * BOARD_CELL_SIZE + BOARD_CELL_SIZE + 1,
                y * BOARD_CELL_SIZE + BOARD_CELL_SIZE + 1
            )

            fill_color = '#994499'

            # Create sprite and add to path sprite cache
            self.path_sprites.add(
                self.canvas.create_rectangle(
                    *coords,
                    fill=fill_color
                )
            )

            self.window.master.controller.references['path_length'].set(
                'Path length: %d' % len(path)
            )
            self.window.master.controller.references['open_set_size'].set(
                'OpenSet size: %d' % open_set
            )
            self.window.master.controller.references['closed_set_size'].set(
                'ClosedSet size: %d' % closed_set
            )
            self.window.master.controller.references['total_set_size'].set(
                'Total set size: %d' % open_set + closed_set
            )

    def clear(self):
        """
        Clears the content area
        """

        self.canvas.delete('all')
        self.window.master.controller.clear_timers()
        self.window.master.controller.clear_stats()

    def destruct(self):
        """
        Destroys this canvas
        """

        self.canvas.delete('all')
        self.canvas.destroy()
