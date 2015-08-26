# -*- coding: utf8 -*-
#
# Created by 'myth' on 8/26/15

import logging

from tkinter import Frame

from common import log, debug


class Main(Frame):
    """
    Main window
    """

    def __init__(self, parent):
        """
        Main window constructor. Takes in a root widget as an argument.
        """

        # Invoke superclass constructor with root widget
        Frame.__init__(self, parent, background='white')

        self.parent = parent

    def set_window_size(self, x=1280, y=600):
        """
        Sets the dimensions of the main window
        """

        self.parent.geometry('%dx%d+0+0' % (x, y))
        debug('Window size set to: %d x %d' % (x, y))

    def maximize_window(self):
        """
        Maximizes the window size
        """

        self.parent.attributes('-zoomed', True)

    def fullscreen_window(self):
        """
        Enables fullscreen window mode
        """

        self.parent.attributes('-fullscreen', True)
