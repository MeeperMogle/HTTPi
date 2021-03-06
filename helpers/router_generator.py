import configparser


def generate():
    parser = configparser.RawConfigParser()
    settings_file = 'settings.properties'
    parser.read(settings_file)
    active_plugins = ', '.join(list(filter(lambda s: s not in ('help', 'no-www'),
                            str(parser.get('plugins', 'active')).split(','))))

    router_filename = 'helpers/router.py'

    router_handle = open(router_filename, 'w')

    router_handle.writelines(
        (
            '#' * 80 + '\n' +
            '# Do not edit this file, it is automatically overwritten at each script start. #\n',
            '#' * 80 + '\n' +
            'from plugins import ' + active_plugins + '\n' +
            'import configparser\n' +
            '\n' +
            'parser = configparser.RawConfigParser()\n' +
            'settings_file = "settings.properties"\n' +
            'parser.read(settings_file)\n' +
            'whitelisted_ips = []\n' +
            'active_plugins = []\n' +
            '\n' +
            '\n' +
            'def handle(args):\n' +
            '    for plugin in str(parser.get("plugins", "active")).split(","):\n' +
            '        active_plugins.append(plugin)\n' +
            '    \n' +
            '    command = args[0]\n' +
            '    \n' +
            '    if command in active_plugins:\n'
        ))

    active_plugins_list = active_plugins.split(', ')
    if len(active_plugins_list) > 0:
        router_handle.write('        if command == "{}":\n'.format(active_plugins_list[0]))
        router_handle.write('            return {}.handle(args[1:])\n'.format(active_plugins_list[0]))

        if len(active_plugins_list) > 1:
            for plugin in active_plugins_list[1:]:
                router_handle.write('        elif command == "{}":\n'.format(plugin))
                router_handle.write('            return {}.handle(args[1:])\n'.format(plugin))
