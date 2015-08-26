# -*- coding: utf8 -*-
#
# Created by 'myth' on 8/26/15

from tkinter import Frame, BOTH


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

    def center_window(self):
        """
        Centers this frame on the screen
        """

        width = 1280
        height = 600

        x = (self.parent.winfo_screenwidth() - width) / 2
        y = (self.parent.winfo_screenheight() - height) / 2

        self.parent.geometry('%dx%d+%d+%d' % (width, height, x, y))
