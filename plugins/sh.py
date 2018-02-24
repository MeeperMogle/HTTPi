import logging
import os
import configparser
import platform
import subprocess

parser = configparser.RawConfigParser()
parser.read('settings.properties')
allowed_commands = str(parser.get('shell', 'allowed.commands')).split(',')


def handle(parameters):
    logging.debug('Entering SH module')
    logging.debug(parameters)

    command = parameters[0]

    result = ccp(command, 'ls', ls, parameters[1:])
    if result is not None:
        return result
    result = ccp(command, 'ls_r', ls_r, parameters[1:])
    if result is not None:
        return result
    result = ccp(command, 'program', program, parameters[1], parameters[2:])
    if result is not None:
        return result


def ccp(input_value, command, callback, *args):
    if input_value == command:
        return callback(args)
    return None


def ls(path):
    actual_path = '/'.join(path)
    return os.listdir(actual_path)


def ls_r(path):
    actual_path = '/'.join(path)
    files = []
    for root, directories, filelist in os.walk(actual_path):
        for file in filelist:
            files.append(root.replace('\\', '/') + '/' + file)
    return files


def program_exists(names):
    for path in names:
        if os.path.exists(path) and os.path.isfile(path):
            return True


def program(args):
    program_name = str(args[0]).replace('%2F', '/')
    global allowed_commands
    if program_name in allowed_commands:
        split_program = program_name.split(' ')
        actual_program = split_program[0]

        if len(split_program) > 1:
            if len(split_program) == 2:
                subprocess.Popen([actual_program, split_program[1], args[1].replace('%2F', '/')])
            elif len(split_program) == 3:
                subprocess.Popen([actual_program, split_program[1], split_program[2], args[1].replace('%2F', '/')])
        else:
            subprocess.Popen([actual_program, args[1].replace('%2F', '/')])
    else:
        logging.warning('Attempt to use non-whitelisted program: ' + program_name + ' ' + ' '.join(args[1]))


def check_os(args):
    return platform.system()
