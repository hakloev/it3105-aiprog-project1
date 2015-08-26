# -*- coding: utf8 -*-
#
# Created by 'myth' on 8/26/15

from tkinter import Menu

### Define menu labels and their commands here
MENUS = [
    (u'Boards', [
        (u'Name', None),
    ]),
    (u'Modes', [
        (u'Mode', None),
    ]),
    (u'Options', [
        (u'Option', None),
    ])
]


def generate_menus(root_menu):
    """
    Takes in the window main menu bar and registers the submenus and
    their commands
    :param root_menu: The main application window menu bar
    """

    # Iterate over the main menu components and their actions
    for name, actions in MENUS:
        menu = Menu(root_menu, tearoff=0)
        root_menu.add_cascade(label=name, menu=menu)

        # Register commands
        for label, cmd in actions:
            menu.add_command(label=label, command=cmd)
