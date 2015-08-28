# -*- coding: utf8 -*-
#
# Created by 'myth' on 8/26/15

import os

from tkinter import Menu

from common import fetch_boards_from_dir


def generate_menus(window):
    """
    Takes in the window main menu bar and registers the submenus and
    their commands
    :param window: The main application window
    """

    ### Define menu labels and their commands here
    menus = [
        (u'Boards', sorted([
            (os.path.basename(board),
             lambda fp=board: window.controller.load_board(file_path=fp)) for board in fetch_boards_from_dir()
        ])),
        (u'Solvers', [
            (u'A*', lambda x='astar': window.controller.solve(algorithm=x)),
        ]),
        (u'Options', [
            (u'Mode', None),
        ])
    ]

    # Iterate over the main menu components and their actions
    for name, actions in menus:
        menu = Menu(window.menu, tearoff=0)
        window.menu.add_cascade(label=name, menu=menu)

        # Register commands
        for label, cmd in actions:
            menu.add_command(label=label, command=cmd)
