# -*- coding: utf8 -*-
#
# Created by 'myth' on 8/26/15

from tkinter import Menu

from main import Controller

### Define menu labels and their commands here
MENUS = [
    (u'Boards', [
        (u'Example 1', Controller.load_board),
    ]),
    (u'Solvers', [
        (u'A*', None),
    ]),
    (u'Options', [
        (u'Mode', None),
    ])
]


def generate_menus(window):
    """
    Takes in the window main menu bar and registers the submenus and
    their commands
    :param window: The main application window
    """

    # Iterate over the main menu components and their actions
    for name, actions in MENUS:
        menu = Menu(window.menu, tearoff=0)
        window.menu.add_cascade(label=name, menu=menu)

        # Register commands
        for label, cmd in actions:
            menu.add_command(label=label, command=cmd)
