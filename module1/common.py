# -*- coding: utf8 -*-
#
# Created by 'myth' on 8/26/15

from datetime import datetime
import logging


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
