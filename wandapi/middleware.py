
import json
import logging
import re
import time

from wandapi import defines, errors
from wandapi.resources import root
import falcon

LOG_API = logging.getLogger('wandapi')

NO_VERSION_URL_REGEX = '^/api/(versions)'

VERSION_PATH_PREFIX = '/api/v'
VERSION_PATH_REGEX = '^/api/v(\d+.\d+|\d+)'

API_PATH_PREFIX = '/api'

EMPTY_REQUEST_BODY_WHITELIST = [
    r'^/api(?:/v1)*/certificates/ssl/regenerate$'
]


class FormatJSON(object):
    """Convert incoming and outgoing data (including time) to JSON."""

    # noinspection PyUnusedLocal
    @classmethod
    def process_request(cls, req, resp):
        """Process incoming request before resource controller."""
        if req.content_length in (None, 0):
            return

        body = req.stream.read()
        if not body:
            raise errors.BadRequestError(defines.ERROR_EMPTY_REQUEST_BODY)

        try:
            req.context['data'] = json.loads(body.decode('utf-8'))
        except (ValueError, UnicodeDecodeError):
            raise errors.BadRequestError(defines.ERROR_INVALID_JSON)

    # noinspection PyMethodMayBeStatic, PyUnusedLocal
    def process_response(self, req, resp, resource):
        """Process response after resource handler and before error handler."""
        if resp.status == falcon.HTTP_NO_CONTENT:
            return

        start_time = req.context.get('start_time')
        elapsed = '{0:.3f}mS'.format(
            (time.time() - start_time) * 1000) if start_time else 'unknown'
        LOG_API.info('%s:%s:%s:%s:%s', req.remote_addr, req.method, req.relative_uri,
                     resp.status, elapsed)

        if resp.body is None:
            result = req.context.get('result')
            body = {'result': result, 'time': elapsed}

            if isinstance(result, list):
                body['count'] = req.context.get('count')
                if not body['count']:
                    body['count'] = len(result)
            else:
                body['count'] = 1

            resp.body = json.dumps(body)
        else:  # pragma: no cover
            # TODO to achieve coverage, mock an API response with invalid JSON and
            # validate log message below
            try:
                json.loads(resp.body)
            except (TypeError, ValueError):
                LOG_API.error('response body is not properly formatted JSON')


class GetVersion(object):
    """Get version from request header."""

    @staticmethod
    def set_req_context_full_path(req):
        # capture the "full length" request path
        req.context['full_req_path'] = '{}{}'.format(API_PATH_PREFIX, req.path)

    # noinspection PyUnusedLocal
    @classmethod
    def process_request(cls, req, resp):
        """Process incoming request before resource handler."""
        # save the unmodified request path
        req.context['full_req_path'] = req.path

        # strip off leading '/api' for un-versioned endpoints
        match = re.search(NO_VERSION_URL_REGEX, req.path)
        if match is not None:
            req.path = req.path[len(API_PATH_PREFIX):]
            return

        # check for version in path first (e.g. 'api/vX')
        match = re.search(VERSION_PATH_REGEX, req.path)
        if match is not None:
            # get the version number from the matching group
            version = match.group()[len(VERSION_PATH_PREFIX):]
            if version not in root.Version.PATH and version not in root.Version.SUPPORTED:
                raise errors.NotFoundError(defines.ERROR_API_VERSION_UNSUPPORTED)
            remainder = req.path[len(match.group()):]
            req.context['remainder'] = remainder
            req.path = '/v{}{}'.format(version.split('.')[0], remainder)
            cls.set_req_context_full_path(req)
            return

        # no version supplied
        raise errors.NotFoundError(defines.ERROR_API_VERSION_NOT_FOUND)


class RequireJSON(object):
    """Require JSON for all request and response data."""

    # noinspection PyUnusedLocal
    @classmethod
    def process_request(cls, req, resp):
        """Process incoming request before resource handler."""
        # Save time for request elapsed time measurement.
        req.context['start_time'] = time.time()

        # Skip JSON check for support bundle downloads or OPTIONS HTTP method.
        if '/files/' in req.path or req.method == 'OPTIONS':
            return

        # Skip JSON check for software uploads.
        if '/switches/software/images' in req.path and req.method == 'PUT':
            return

        # Skip JSON check for backup uploads.
        if '/backups/upload' in req.path and req.method == 'POST':
            return

        # Ensure client accepts the JSON format.
        accept = req.get_header('Accept')
        if accept is None or ('application/json' not in accept and '*/*' not in accept):
            raise errors.UnacceptableError(defines.ERROR_ONLY_JSON_RESPONSE)

        # Ensure incoming data format is JSON.
        if req.method in ('POST', 'PUT', 'PATCH'):
            if req.content_type is None or 'application/json' not in req.content_type:
                raise errors.UnsupportedMediaTypeError(defines.ERROR_ONLY_JSON_REQUESTS)

            if (req.content_length in (None, 0) and
                    not re.search('|'.join(EMPTY_REQUEST_BODY_WHITELIST), req.path)):
                raise errors.BadRequestError(defines.ERROR_EMPTY_REQUEST_BODY)
