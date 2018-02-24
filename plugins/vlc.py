import configparser

import pyautogui
import logging
from plugins.mv import window_focus, window_minimise, window_maximise
from plugins.sh import program, allowed_commands, check_os, ls_r, program_exists

vlc_window_name = 'VLC media player'

parser = configparser.RawConfigParser()
parser.read('settings.properties')
video_folders = str(parser.get('directories', 'videos')).split(',')
video_extensions = str(parser.get('vlc', 'vlc.extensions')).split(',')
exe_paths = str(parser.get('vlc', 'executable.paths')).split(',')


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

    result = ccp(command, 'play_pause', play_pause)
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

    result = ccp(command, 'maximise', maximise)
    if result is not None:
        return result

    result = ccp(command, 'exists', exists)
    if result is not None:
        return result

    result = ccp(command, 'list_videofiles', list_videofiles)
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


def focus():
    return window_focus(vlc_window_name)


def exists():
    if program_exists(exe_paths):
        return True


def focus_fullscreen():
    return focus() + ' & ' + enter_fullscreen()


def minimise():
    return window_minimise(vlc_window_name)


def maximise():
    return window_maximise(vlc_window_name)


def toggle_mute():
    focus()
    p('m')
    return 'Muting'


def enter_fullscreen():
    focus()
    p('f')
    return 'Toggling fullscreen'


def leave_fullscreen():
    focus()
    p('esc')
    return 'Leaving fullscreen'


def play_pause():
    focus()
    p('space')
    return 'Toggling play/pause'


def next_video():
    focus()
    p('n')
    return 'Next video'


def previous_video():
    focus()
    p('p')
    return 'Previous video'


def stop():
    focus()
    p('s')
    return 'Stop'


def show_position():
    focus()
    p('t')
    return 'Show position'


def volume_up():
    focus()
    pyautogui.hotkey('ctrl', 'up')
    return 'Volume up'


def volume_down():
    focus()
    pyautogui.hotkey('ctrl', 'down')
    return 'Volume down'


def toggle_interface():
    focus()
    p('i')
    return 'Toggle interface'


def snapshot():
    focus()
    pyautogui.hotkey('shift', 's')
    return 'Snapshot taken'


def list_videofiles():
    all_video_files = []

    for folder in video_folders:
        for file in ls_r([folder, '']):
            all_video_files.append(file)

    all_video_files = list(filter(lambda s: s.split('.')[-1] in video_extensions, all_video_files))

    return all_video_files


def open_file(file_path):
    vlc_commands = list(filter(lambda s: 'vlc' in s, allowed_commands))

    if check_os('') == 'Windows':
        vlc_commands = list(filter(lambda s: '.exe' in s, vlc_commands))
    else:
        vlc_commands = list(filter(lambda s: '.exe' not in s, vlc_commands))

    if len(vlc_commands) > 0:
        vlc_command = vlc_commands[0]
        program([vlc_command, file_path])
        return 'Opening file using ' + vlc_command

    return 'Could not find appropriate vlc command'
