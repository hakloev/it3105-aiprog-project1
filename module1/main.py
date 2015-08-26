# -*- coding: utf-8 -*-

import logging
import datetime

from tkinter import Tk

from gui.window import Main

if __name__ == '__main__':
    """
    Application start sequence
    """

    logging.basicConfig(filename='debug.log', level=logging.DEBUG)
    logging.debug('Starting application at %s' % datetime.datetime.now().strftime('%H:%M:%S'))

    root = Tk()
    # Render the main window
    main = Main(root)

    # Start application
    root.mainloop()
