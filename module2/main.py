# -*- coding: utf8 -*-
#
# Created by 'myth' on 9/23/15

import logging

from gui.alternatives import *
from common import *
from controller import MainController
from gui.window import Main
from gui.render import GraphRenderer


if __name__ == '__main__':
    """
    Application start sequence
    """

    logging.basicConfig(filename='debug.log', level=logging.DEBUG)
    log('Starting application')

    root = Tk()
    root.wm_title('A*-GAC')
    root.wm_protocol('WM_DELETE_WINDOW', root.quit())

    # Render the main window
    main = Main(root, MainController(), name='main')
    main.controller.set_window(main)

    # Set the initial renderer
    main.set_renderer(GraphRenderer(main.content_area, figsize=(8, 7)))

    # Register menubar components
    generate_menus(main)

    # Generate stats and options pane
    generate_options(main.options_area)
    generate_stats(main.stats_area)
    main.grid(row=0, column=0)

    # Start application
    root.mainloop()
