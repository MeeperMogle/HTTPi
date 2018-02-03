import pyautogui
import logging


def handle(parameters):
    logging.debug('Entering MV')
    logging.debug(parameters)

    command = parameters[0]
