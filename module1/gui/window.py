# -*- coding: utf8 -*-
#
# Created by 'myth' on 8/26/15

from tkinter import Frame, BOTH, Menu, messagebox

from common import log, debug


class Main(Frame):
    """
    Main window
    """

    def __init__(self, parent, controller):
        """
        Main window constructor. Takes in a root widget as an argument.
        """

        # Invoke superclass constructor with root widget
        Frame.__init__(self, parent, background='white')

        menu = Menu(parent)

        self.parent = parent
        self.menu = menu
        self.renderer = None
        self.controller = controller

        parent.config(menu=menu)
        parent.title('A*')

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

    def set_renderer(self, renderer):
        """
        Sets the active renderer to this window
        """

        debug('Setting renderer to %s' % renderer)

        if self.renderer and renderer is not self.renderer:
            debug('Destroying and replacing old renderer: %s' % self.renderer)
            self.renderer.destruct()
        self.renderer = renderer

    def render(self, *args, **kwargs):
        """
        Renders the main content area, based on a provided render function
        """

        if self.renderer:
            self.renderer.render_board(*args, **kwargs)
            self.pack(fill=BOTH)

            debug('Main.render() called')
        else:
            messagebox.showerror(
                'Missing renderer',
                'Main.render() invoked without renderer set'
            )
            log('Main.render() invoked without renderer set')
