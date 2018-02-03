import pyautogui
import logging


def handle(parameters):
    logging.debug('Entering MV module')
    logging.debug(parameters)

    command = parameters[0]

    result = ccp(command, 'left', move_left, parameters[1])
    if result is not None:
        return result
    result = ccp(command, 'right', move_right, parameters[1])
    if result is not None:
        return result
    result = ccp(command, 'up', move_up, parameters[1])
    if result is not None:
        return result
    result = ccp(command, 'down', move_down, parameters[1])
    if result is not None:
        return result
    result = ccp(command, 'to', move_to, parameters[1:3])
    if result is not None:
        return result


def ccp(input_value, command, callback, args):
    if input_value == command:
        return callback(args)
    return None


def get_screen_size():
    return pyautogui.size()


def get_screen_width():
    return get_screen_size()[0]


def get_screen_height():
    return get_screen_size()[1]


def move_to(xy):
    x = int(xy[0])
    y = int(xy[1])
    x = get_screen_width() if x > get_screen_width() else x
    y = get_screen_height() if y > get_screen_height() else y
    x = 0 if x < 0 else x
    y = 0 if y < 0 else y

    pyautogui.moveTo(x, y)
    return 'Moved to ' + str(pyautogui.position())


def move_up(px):
    px = int(px)
    if px < 0:
        return move_down(px)

    pyautogui.moveRel(0, -px)
    return 'Moved ' + str(px) + ' up, to ' + str(pyautogui.position())


def move_down(px):
    px = int(px)
    if px < 0:
        return move_up(px)

    pyautogui.moveRel(0, px)
    return 'Moved ' + str(px) + ' down, to ' + str(pyautogui.position())


def move_left(px):
    px = int(px)
    if px < 0:
        return move_right(px)

    pyautogui.moveRel(-px, 0)
    return 'Moved ' + str(px) + ' left, to ' + str(pyautogui.position())


def move_right(px):
    px = int(px)
    if px < 0:
        return move_left(px)

    pyautogui.moveRel(px, 0)
    return 'Moved ' + str(px) + ' right, to ' + str(pyautogui.position())

