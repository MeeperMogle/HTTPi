#!/usr/bin/env python3
import configparser
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer

from helpers import router  # Will be generated on startup of script
from helpers import router_generator

parser = configparser.RawConfigParser()
whitelisted_ips = []
active_plugins = []


def start_page(plugin_name):
    start_html_file = 'start_pages/' + plugin_name + '.html'
    html = ''

    with open('start_pages/common/header.html', 'r') as f:
        html += f.read()
    with open(start_html_file, 'r') as f:
        html += f.read()
    with open('start_pages/common/footer.html', 'r') as f:
        html += f.read()
    return html


class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        target = str(self.path)[1:]
        self._set_response()

        if 'favicon.ico' in str(self.requestline):
            return

        client_ip = str(self.client_address[0])
        if client_ip not in whitelisted_ips:
            self.wfile.write('{} not in whitelist'.format(client_ip).encode('utf-8'))
            logging.warning('Non-whitelisted {} attempted to access /{}'.format(client_ip, target))
            return

        logging.info('{} => /{}'.format(client_ip, target))

        command_bits = target.split('/')
        self.handle_plugin(command_bits)

    def do_POST(self):
        pass

    def handle_plugin(self, command_bits):
        plugin_name = command_bits[0]

        www_enabled = 'no-www' not in active_plugins

        if plugin_name == '' and www_enabled:
            with open('start_pages/common/index.html', 'r') as f:
                response = f.read()
                log_response = 'Served index.html'
        elif plugin_name not in active_plugins:
            response = 'No active plugin "{}"'.format(plugin_name)
            log_response = 'No active plugin "{}, could not load"'.format(plugin_name)
        elif plugin_name == 'help' and www_enabled:
            response = start_page('help/' + command_bits[1].lower() + '_help')
            log_response = 'Served help page for ' + command_bits[1]
        elif www_enabled and (len(command_bits) == 1 or len(command_bits) == 2 and command_bits[1] == ''):
            response = start_page(plugin_name)
            log_response = 'Served index for ' + plugin_name
        elif len(command_bits) > 1:
            response = router.handle(command_bits)
            log_response = response
        else:
            response = ''
            log_response = 'No action for ' + str(command_bits)

        self.wfile.write(str(response).encode('utf-8'))

        if 'screenshot' not in command_bits:
            logging.info(log_response)
        else:
            logging.ino('-- Screenshot omitted --')


def run():
    setup_logging()

    settings_file = 'settings.properties'
    parser.read(settings_file)
    load_properties()

    try:
        port = parser.get('server', 'port')
    except configparser.NoOptionError:
        port = '8080'

    router_generator.generate()

    server_address = ('', int(port))
    httpd = HTTPServer(server_address, S)
    logging.info('Starting httpd on port {}...'.format(port))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...')


def setup_logging():
    logging.basicConfig(level=logging.INFO)
    log_formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s --- %(msg)s')
    root_logger = logging.getLogger()
    file_handler = logging.FileHandler('access.log')
    console_handler = logging.StreamHandler()
    file_handler.setFormatter(log_formatter)
    console_handler.setFormatter(log_formatter)
    root_logger.removeHandler(root_logger.handlers[0])
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)


def load_properties():
    logging.info('Loading properties...')
    for ip in str(parser.get('security', 'ip_whitelist')).split(','):
        whitelisted_ips.append(ip)

    for plugin in str(parser.get('plugins', 'active')).split(','):
        active_plugins.append(plugin)


if __name__ == '__main__':
    run()
