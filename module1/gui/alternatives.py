# -*- coding: utf8 -*-
#
# Created by 'myth' on 8/26/15

import os

from tkinter import *

from common import fetch_boards_from_dir
from gui.render import GUI_UPDATE_INTERVAL

ASTAR_OPTIONS = [
    'best',
    'bfs',
    'dfs'
]


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
        ])
    ]

    # Iterate over the main menu components and their actions
    for name, actions in menus:
        menu = Menu(window.menu, tearoff=0)
        window.menu.add_cascade(label=name, menu=menu)

        # Register commands
        for label, cmd in actions:
            menu.add_command(label=label, command=cmd)


def generate_options(frame, *args, **kwargs):
    """
    Generates options for
    :param frame: Stats and options frame reference
    """

    mode_label = Label(frame, text='Algorithm mode:')
    mode_label.grid(row=0, padx=5, pady=5, ipadx=5, ipady=5, sticky='W')

    mode_var = StringVar(master=frame, value=ASTAR_OPTIONS[0], name='algorithm_mode')
    frame.master.controller.references['algorithm_mode'] = mode_var
    options = OptionMenu(frame, mode_var, *tuple(ASTAR_OPTIONS))
    options.grid(row=0, column=1, sticky='E')

    update_interval_label = Label(frame, text='Update interval (ms):')
    update_interval_label.grid(row=1, padx=5, pady=5, ipadx=5, ipady=5, sticky='W')

    update_interval = Entry(frame)
    update_interval.insert(0, str(GUI_UPDATE_INTERVAL))
    update_interval.grid(row=1, column=1, padx=5, pady=5, ipadx=5, ipady=5, sticky='E')
    frame.master.controller.references['update_interval'] = update_interval


def generate_stats(frame, *args, **kwargs):
    """
    Generates and fills the Statistics LabelFrame
    """

    path_length = StringVar(frame)
    path_length.set('Path length: 0')
    path_length_label = Label(frame, textvariable=path_length)
    frame.master.controller.references['path_length'] = path_length
    path_length_label.grid(row=0, padx=5, pady=5, ipadx=5, ipady=5, sticky='W')

    open_set_size = StringVar(frame)
    open_set_size.set('OpenSet size: 0')
    open_set_size_label = Label(frame, textvariable=open_set_size)
    frame.master.controller.references['open_set_size'] = open_set_size
    open_set_size_label.grid(row=1, padx=5, pady=5, ipadx=5, ipady=5, sticky='W')

    closed_set_size = StringVar(frame)
    closed_set_size.set('ClosedSet size: 0')
    closed_set_size_label = Label(frame, textvariable=closed_set_size)
    frame.master.controller.references['closed_set_size'] = closed_set_size
    closed_set_size_label.grid(row=2, padx=5, pady=5, ipadx=5, ipady=5, sticky='W')

    total_set_size = StringVar(frame)
    total_set_size.set('Total set size: 0')
    total_set_size_label = Label(frame, textvariable=total_set_size)
    frame.master.controller.references['total_set_size'] = total_set_size
    total_set_size_label.grid(row=3, padx=5, pady=5, ipadx=5, ipady=5, sticky='W')
