
import eventlet  # noqa: I202 monkey patching must happen first

# While the thread module is monkey patched, you may still use eventlet-
# friendly thread constructs i.e. eventlet.greenthread and eventlet.queue.
eventlet.monkey_patch(os=True,
                      select=True,
                      socket=True,
                      thread=True,
                      psycopg=True,
                      time=True)

import logging  # noqa: I100
from logging import config as logging_config  # noqa: I100
from wsgiref import simple_server  # noqa: I100

from wandapi import config, errors, middleware  # noqa: I100
import falcon  # noqa: I100
from wandapi.resources import init_config, root, v1  # noqa: I100


def setup_app(conf=config):
    """Perform falcon application setup."""
    api = falcon.API(middleware=[
        middleware.RequireJSON(),
        middleware.FormatJSON(),
        middleware.GetVersion(),
    ])

    # handle all errors
    api.add_error_handler(Exception, errors.WandaError.handle)

    # initialize application
    init_config(conf.wanda['base_dir'])
    logging_config.dictConfig(conf.logging)
    api_setup_logger = logging.getLogger('wanda_setup')

    # un-versioned resources
    api.add_route('/versions', root.Version())

    api.add_route('/v1/wands', v1.wands.WandCollection())
    api.add_route('/v1/wands/{uuid}', v1.wands.WandItem())

    api_setup_logger.info('API Initialized')

    return api


if __name__ == '__main__':  # pragma: no cover
    """Simple server for debugging."""
    httpd = simple_server.make_server('127.0.0.1', 8000, setup_app(config))
    httpd.serve_forever()
