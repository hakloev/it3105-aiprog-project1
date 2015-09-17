# -*- coding: utf8 -*-
#
# Created by 'myth' on 8/26/15

from datetime import datetime
import logging
import os


def log(message):
    """
    Logs a message to the logger system
    :param message: The log message to be stored
    """

    logging.info('\t[%s] %s' % (datetime.now().strftime('%H:%M:%S'), message))


def debug(message):
    """
    Logs a debug message to the logger system
    :param message: The debug message to be stored
    """

    logging.debug('\t[%s] %s' % (datetime.now().strftime('%H:%M:%S'), message))


def fetch_boards_from_dir(rootdir='boards'):
    """
    Returns a list of paths to the pre-defined boards in the boards directory
    :return: A list of directories
    """

    boards = []
    boards_dir = os.path.join(os.path.dirname(__file__), rootdir)

    for board in os.listdir(boards_dir):
        full_path = os.path.join(boards_dir, board)
        if os.path.isfile(full_path):
            boards.append(full_path)

    return boards


def make_func(var_names, expression, environment=globals()):
    """
    This function lets the user input constraint descriptions, at runtime, and
    converting them into working code chunks
    :param var_names: The variables for the constraints
    :param expression: The expression to evaluate
    :param environment:
    :return:
    """
    args = ""
    for n in var_names:
        args = args + "," + n
    return eval("(lambda " + args[1:] + ": " + expression + ")", environment)