import falcon
import jwt

from knoweak.settings import AUTH


class AuthenticationMiddleware:

    def __init__(self, free_access_routes=None):
        self.free_access_routes = free_access_routes or []

    def process_resource(self, req, resp, resource, params):
        if AUTH['disabled']:
            return
        if req.method == 'OPTIONS':
            return  # CORS support
        if req.path in self.free_access_routes:
            return

        auth_header_parts = _validate_header(req)
        decoded_token = _validate_token(auth_header_parts[1])

        req.user = {
            'scope': decoded_token.get('scope')
        }


def _validate_header(req):
    auth_header = req.get_header('Authorization')
    if not auth_header:
        raise falcon.HTTPUnauthorized(description='Missing credentials.')

    auth_header_parts = auth_header.split(' ', 1)
    if not auth_header_parts[0] == 'Bearer':
        raise falcon.HTTPUnauthorized(description='Invalid authentication scheme. Expected value: Bearer.')
    if len(auth_header_parts) == 1:
        raise falcon.HTTPUnauthorized(description='Missing access token.')

    return auth_header_parts


def _validate_token(token):
    try:
        decoded_token = jwt.decode(token, key=AUTH['secret_key'], algorithms='HS256', options={'verify_aud': False})
    except Exception as e:
        raise falcon.HTTPUnauthorized(description=f'Invalid access token. {str(e)}.')
    return decoded_token


def check_scope(req, resp, resource, params, allowed_scope=None):
    """Falcon hook.
    Checks if allowed scope registered for responder (or for resource) exist in requested scope.
    If yes, the request will continue to be processed. Otherwise, it will raise a 403 (Forbidden) error.

    :param req: Falcon.Request object from which the requested scope will be retrieved.
    :param resp: Not used. Mandatory for hook functions.
    :param resource: Not used. Mandatory for hook functions.
    :param params: Not used. Mandatory for hook functions.
    :param allowed_scope: The permission(s) allowed for Falcon responder or for entire resource.
        It must be a string with permissions separated by space.
        If None (default) or empty, there will be no access restriction and the effect will be the
        same as if the hook was not applied.
    """
    if not allowed_scope or AUTH['disabled']:
        return

    user = getattr(req, 'user', {})
    requested_scopes = user.get('scope', '').split(' ')
    allowed_scopes = allowed_scope.split(' ')

    if not set(allowed_scopes).issubset(requested_scopes):
        raise falcon.HTTPForbidden(description='Check your permission to perform this action.')
