# -*- coding: utf-8 -*-

import logging

from tkinter import Tk

from common import log, debug
from gui import window, menu, render

if __name__ == '__main__':
    """
    Application start sequence
    """

    logging.basicConfig(filename='debug.log', level=logging.DEBUG)
    log('Starting application')

    root = Tk()

    # Render the main window
    main = window.Main(root)
    main.set_window_size(x=1024, y=500)

    # Register menubar components
    menu.generate_menus(main.menu)

    # Set the initial renderer
    main.set_renderer(render.CanvasRenderer(main))
    main.render()

    # Start application
    root.mainloop()
