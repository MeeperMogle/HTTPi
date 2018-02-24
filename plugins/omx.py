import configparser
import logging

import pyautogui

from plugins.sh import program, ls_r

parser = configparser.RawConfigParser()
parser.read('settings.properties')
video_folders = str(parser.get('directories', 'videos')).split(',')
video_extensions = str(parser.get('omx', 'omx.extensions')).split(',')

#    -l  --pos n                 Start position (hh:mm:ss)


def handle(parameters):
    logging.debug('Entering OMX module')
    logging.debug(parameters)

    command = parameters[0]

    result = ccp(command, 'list_videofiles', list_videofiles)
    if result is not None:
        return result

    result = ccp(command, 'play_pause', play_pause)
    if result is not None:
        return result

    result = ccp(command, 'volume_down', volume_down)
    if result is not None:
        return result

    result = ccp(command, 'volume_up', volume_up)
    if result is not None:
        return result

    result = ccp(command, 'rewind', rewind)
    if result is not None:
        return result

    result = ccp(command, 'fast_forward', fast_forward)
    if result is not None:
        return result

    result = ccp(command, 'information', information)
    if result is not None:
        return result

    result = ccp(command, 'toggle_subtitles', toggle_subtitles)
    if result is not None:
        return result

    result = ccp(command, 'exit', exit_omx)
    if result is not None:
        return result

    result = ccp(command, 'small_back', small_back)
    if result is not None:
        return result

    result = ccp(command, 'small_forward', small_forward)
    if result is not None:
        return result

    result = ccp(command, 'big_back', big_back)
    if result is not None:
        return result

    result = ccp(command, 'big_forward', big_forward)
    if result is not None:
        return result

    if command == 'open' and len(parameters) > 1:
        return open_file(parameters[1])

    return 'Command not found'


def ccp(input_value, command, callback):
    if input_value == command:
        return callback()
    return None


def p(text):
    pyautogui.press(text)


def play_pause():
    p('p')
    return 'Toggling play/pause'


def volume_down():
    p('-')
    return 'Decreasing volume'


def volume_up():
    p('+')
    return 'Increasing volume'


def rewind():
    p('<')
    return 'Rewinding'


def fast_forward():
    p('>')
    return 'Fast-forwarding'


def information():
    p('z')
    return 'Showing information'


def toggle_subtitles():
    p('s')
    return 'Toggling subtitles'


def exit_omx():
    p('q')
    return 'Exiting OMXplayer'


def small_back():
    p('left')
    return 'Jumping -30 sec'


def small_forward():
    p('right')
    return 'Jumping +30 sec'


def big_back():
    p('down')
    return 'Jumping -10 min'


def big_forward():
    p('up')
    return 'Jumping +10 min'


def list_videofiles():
    all_video_files = []

    for folder in video_folders:
        for file in ls_r([folder, '']):
            all_video_files.append(file)

    all_video_files = list(filter(lambda s: s.split('.')[-1] in video_extensions, all_video_files))

    return all_video_files


def open_file(file_path):
    program(['lxterminal -e omxplayer', file_path])
