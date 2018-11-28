
import json
import logging
import time

import falcon

LOG = logging.getLogger('wandapi')


class WandaError(Exception):
    """Base error class."""

    # noinspection PyUnusedLocal
    @staticmethod
    def handle(ex, req, resp, params):

        # default error message sent to the client is simply the exception string
        message = str(ex)

        if isinstance(ex, BadRequestError):
            status = falcon.HTTP_BAD_REQUEST
        elif isinstance(ex, ForbiddenError):
            status = falcon.HTTP_FORBIDDEN
        elif isinstance(ex, InternalError):
            status = falcon.HTTP_INTERNAL_SERVER_ERROR
        elif isinstance(ex, falcon.HTTPInvalidParam):
            status = falcon.HTTP_BAD_REQUEST
            message = str(ex.description)
        elif isinstance(ex, falcon.HTTPMethodNotAllowed):
            status = falcon.HTTP_METHOD_NOT_ALLOWED
        elif isinstance(ex, falcon.HTTPNotFound):
            status = falcon.HTTP_NOT_FOUND
        elif isinstance(ex, NotFoundError):
            status = falcon.HTTP_NOT_FOUND
        elif isinstance(ex, UnacceptableError):
            status = falcon.HTTP_NOT_ACCEPTABLE
        elif isinstance(ex, UnauthorizedError):
            status = falcon.HTTP_UNAUTHORIZED
        elif isinstance(ex, UnsupportedMediaTypeError):
            status = falcon.HTTP_UNSUPPORTED_MEDIA_TYPE
        elif isinstance(ex, MalformedPatchDocument):
            status = falcon.HTTP_BAD_REQUEST
        elif isinstance(ex, ConcurrentModification):
            status = falcon.HTTP_CONFLICT
        elif isinstance(ex, UnProcessableRequestError):
            status = falcon.HTTP_UNPROCESSABLE_ENTITY
        elif isinstance(ex, TokenExpiredError):
            # not (yet) defined in falcon...
            status = '419 Authentication Timeout'
        elif isinstance(ex, AcceptedBusy):
            status = falcon.HTTP_ACCEPTED
        else:  # pragma: no cover
            LOG.exception('Unhandled Exception {} {}'.format(type(ex), ex))
            status = falcon.HTTP_INTERNAL_SERVER_ERROR
            message = 'Internal Server Error'

        if not message and status != falcon.HTTP_NOT_FOUND:
            LOG.exception('Empty error message for {} {}'.format(type(ex), ex))

        # Handle the special case of HTTP Status 202, which is not really an error
        # Force 'result' to be an empty list, and provide message to be passed in response
        if status == falcon.HTTP_ACCEPTED:
            body = {'result': [], 'message': message}
        else:
            body = {'result': message}

        # add API call time if a request start time was recorded
        start_time = req.context.get('start_time')
        elapsed = '{0:.3f}mS'.format((time.time() - start_time) * 1000) if start_time else 'unknown'
        LOG.info('%s:%s:%s:%s:%s:%s', req.remote_addr, req.method, req.path, status, str(ex),
                 elapsed)
        body['time'] = elapsed

        resp.status = status
        resp.body = json.dumps(body)
        resp.set_header('Content-Type', 'application/json')
        resp.set_header('Content-Length', str(len(resp.body)))


class BadRequestError(WandaError):
    """Incorrect or bad data in request."""

    pass


class ForbiddenError(WandaError):
    """Insufficient privileges to perform request."""

    pass


class InternalError(WandaError):
    """Internal error performing request."""

    pass


class NotFoundError(WandaError):
    """The requested item was not found."""

    pass


class TokenExpiredError(WandaError):
    """Token has expired."""

    pass


class UnacceptableError(WandaError):
    """Incorrect request header."""

    pass


class UnauthorizedError(WandaError):
    """Authentication failed or required to perform request."""

    pass


class UnsupportedMediaTypeError(WandaError):
    """Unsupported media type in request."""

    pass


class MalformedPatchDocument(WandaError):
    """Malformed Patch Document."""

    pass


class ConcurrentModification(WandaError):
    """Concurrent Modification Document."""

    pass


class UnProcessableRequestError(WandaError):
    """UnProcessable Request Error."""

    pass


class AcceptedBusy(WandaError):
    """Request accepted but system busy."""

    pass
