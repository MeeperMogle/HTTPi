import base64

import pyautogui
import logging
from urllib.parse import unquote
from PIL import Image


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
    result = ccp(command, 'center', center, '')
    if result is not None:
        return result
    result = ccp(command, 'click', click, parameters[1])
    if result is not None:
        return result
    result = ccp(command, 'write', write, parameters[1])
    if result is not None:
        return result
    result = ccp(command, 'window_focus', window_focus, parameters[1])
    if result is not None:
        return result
    result = ccp(command, 'screenshot', screenshot, parameters[1])
    if result is not None:
        return result
    result = ccp(command, 'size', screen_size, parameters[1])
    if result is not None:
        return result


def ccp(input_value, command, callback, args):
    if input_value == command:
        return callback(args)
    return None


def find_window(title_contents):
    try:
        visible_windows = pyautogui.getWindows()
        for title in visible_windows:
            if title_contents in title:
                return pyautogui.Window(visible_windows[title])
    except AttributeError as e:
        if "has no attribute 'getWindows" in str(e):
            from libs._window_x11 import Window, getWindows, getWindow
            visible_windows = getWindows()
            for title in visible_windows:
                if title_contents in title:
                    return Window(visible_windows[title])
            pass
    return None


def window_focus(title_contents):
    found_window = find_window(title_contents)
    if found_window is not None:
        found_window.set_foreground()
        found_window.restore()
        return 'Moving focus to window: ' + title_contents

    return 'Could not locate window: ' + title_contents


def window_minimise(title_contents):
    found_window = find_window(title_contents)
    if found_window is not None:
        found_window.set_foreground()
        found_window.minimize()
        return 'Minimising window: ' + title_contents

    return 'Could not locate window: ' + title_contents


def window_maximise(title_contents):
    found_window = find_window(title_contents)
    if found_window is not None:
        found_window.set_foreground()
        found_window.maximize()
        return 'Maximising window: ' + title_contents

    return 'Could not locate window: ' + title_contents


def center(args):
    center_of_screen = (int(get_screen_width() / 2), int(get_screen_height() / 2))
    move_to(center_of_screen)
    return 'Moved to center of screen ' + str(center_of_screen)


def click(method):
    if method == 'left':
        pyautogui.click()
    elif method == 'right':
        pyautogui.rightClick()
    elif method == 'middle':
        pyautogui.middleClick()
    elif method == 'double':
        pyautogui.doubleClick()
    else:
        return 'Unknown click method: ' + method
    return 'Performed ' + method + ' click'


def write(text):
    text = unquote(str(text))
    text_parts = text.split('|||')

    special_characters = ('enter',)

    for part in text_parts:
        if part in special_characters:
            pyautogui.press(part)
        else:
            pyautogui.typewrite(part)

    return text


def screenshot(args):
    screen = pyautogui.screenshot()

    cursor_image = Image.open('img/cursor.jpg')
    screen.paste(im=cursor_image, box=pyautogui.position())
    screen.save('img/state.png')

    with open('img/state.png', 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return encoded_string


def screen_size(args):
    return pyautogui.size()


def draw_pointer_at(xy, image):
    x = xy[0]
    y = xy[1]
    black = (0, 0, 0)
    white = (255, 255, 255)
    for i in range(15):
        image.putpixel((x, y + i), black)
    return image


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

