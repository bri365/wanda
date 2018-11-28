import logging

from wandapi import api, config
import eventlet
from eventlet import listen, wsgi

DEFAULT_MAX_SIMULTANEOUS_API_REQUESTS = 500
# ensure the below is tuned to match the upstream webserver (nginx.conf large_client_header_buffers)
DEFAULT_URL_LENGTH_LIMIT = 65536
LOG = logging.getLogger('wandapi')


def run_server():
    """Start the server."""
    host = config.server['host']
    port = config.server['port']

    max_pool_size = DEFAULT_MAX_SIMULTANEOUS_API_REQUESTS
    worker_pool = eventlet.GreenPool(max_pool_size)
    sock = listen((host, int(port)))

    app = api.setup_app(config)

    # socket, app, log
    wsgi.server(sock, app, custom_pool=worker_pool, url_length_limit=DEFAULT_URL_LENGTH_LIMIT)
    return 0


def main():  # pragma: no cover
    """Main."""
    # noinspection PyBroadException
    try:
        return run_server()
    except SystemExit as exit_code:
        return exit_code
