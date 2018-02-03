import pyautogui
import logging
from plugins.mv import window_focus, window_minimise

vlc_window_name = 'VLC media player'


def focus():
    return window_focus(vlc_window_name)


def focus_fullscreen():
    return focus() + ' & ' + enter_fullscreen()


def minimise():
    return window_minimise(vlc_window_name)


def handle(parameters):
    logging.debug('Entering VLC module')
    logging.debug(parameters)

    command = parameters[0]

    result = ccp(command, 'toggle_mute', toggle_mute)
    if result is not None:
        return result

    result = ccp(command, 'enter_fullscreen', enter_fullscreen)
    if result is not None:
        return result

    result = ccp(command, 'leave_fullscreen', leave_fullscreen)
    if result is not None:
        return result

    result = ccp(command, 'pause', pause)
    if result is not None:
        return result

    result = ccp(command, 'play', play)
    if result is not None:
        return result

    result = ccp(command, 'next_video', next_video)
    if result is not None:
        return result

    result = ccp(command, 'previous_video', previous_video)
    if result is not None:
        return result

    result = ccp(command, 'stop', stop)
    if result is not None:
        return result

    result = ccp(command, 'show_position', show_position)
    if result is not None:
        return result

    result = ccp(command, 'volume_up', volume_up)
    if result is not None:
        return result

    result = ccp(command, 'volume_down', volume_down)
    if result is not None:
        return result

    result = ccp(command, 'toggle_interface', toggle_interface)
    if result is not None:
        return result

    result = ccp(command, 'snapshot', snapshot)
    if result is not None:
        return result

    result = ccp(command, 'focus', focus)
    if result is not None:
        return result

    result = ccp(command, 'focus_fullscreen', focus_fullscreen)
    if result is not None:
        return result

    result = ccp(command, 'minimise', minimise)
    if result is not None:
        return result

    return 'Command not found'


def ccp(input_value, command, callback):
    if input_value == command:
        return callback()
    return None


def p(text):
    pyautogui.press(text)


def toggle_mute():
    p('m')
    return 'Muting'


def enter_fullscreen():
    pos_start_menu = pyautogui.locateOnScreen('images/start_button.png')
    if pos_start_menu is not None:
        p('f')
        return 'Entering fullscreen'
    return 'Already in fullscreen'


def leave_fullscreen():
    p('esc')
    return 'Leaving fullscreen'


def pause():
    p('[')
    return 'Pausing'


def play():
    p(']')
    return 'Playing'


def next_video():
    p('n')
    return 'Next video'


def previous_video():
    p('p')
    return 'Previous video'


def stop():
    p('s')
    return 'Stop'


def show_position():
    p('t')
    return 'Show position'


def volume_up():
    pyautogui.hotkey('ctrl', 'up')
    return 'Volume up'


def volume_down():
    pyautogui.hotkey('ctrl', 'down')
    return 'Volume down'


def toggle_interface():
    p('i')
    return 'Toggle interface'


def snapshot():
    p('s')
    return 'Snapshot taken'


