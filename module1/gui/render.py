# -*- coding: utf8 -*-
#
# Created by 'myth' on 8/26/15

from tkinter import Canvas, BOTH


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

    def destruct(self):
        """
        Destroys this renderer
        """

        pass


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
        self.canvas.config(bg='red')
        self.canvas.pack(fill=BOTH, expand=1)

    def render(self):
        """
        Renders the data
        """

        self.clear()
        pass

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
