#!/usr/bin/env python3
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
from plugins import vlc
import configparser

parser = configparser.RawConfigParser()
whitelisted_ips = []
active_plugins = []


def handle(text, callback, *targets):
    if type(targets) == str:
        targets = (targets,)

    if text in targets:
        callback()


def start_page(plugin_name):
    start_html_file = 'start_pages/' + plugin_name + '.html'
    html = ''

    with open('start_pages/header.html', 'r') as f:
        html += f.read()
    with open(start_html_file, 'r') as f:
        html += f.read()
    with open('start_pages/footer.html', 'r') as f:
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

        if plugin_name == '':
            with open('start_pages/index.html', 'r') as f:
                response = f.read()
        elif plugin_name not in active_plugins:
            self.wfile.write('No active plugin "{}"'.format(plugin_name).encode('utf-8'))
            return
        elif len(command_bits) == 1 or len(command_bits) == 2 and command_bits[1] == '':
            response = start_page(plugin_name)
        elif plugin_name == 'std':
            response = vlc.handle(command_bits[1:])
        elif plugin_name == 'vlc':
            response = vlc.handle(command_bits[1:])
        else:
            response = 'Nothing to do'

        self.wfile.write(str(response).encode('utf-8'))


class PishHTTPServer(HTTPServer):
    pass


def run(port=1337):
    setup_logging()

    settings_file = 'settings.properties'
    parser.read(settings_file)
    load_properties()

    server_address = ('', port)
    httpd = HTTPServer(server_address, S)
    logging.info('Starting httpd...')
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
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
