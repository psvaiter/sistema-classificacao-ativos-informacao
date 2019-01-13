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
        _validate_scopes(resource, decoded_token)


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
        decoded_token = jwt.decode(token, key=AUTH['secret_key'], algorithms='HS256')
    except Exception as e:
        raise falcon.HTTPUnauthorized(description=f'Invalid access token. {str(e)}.')
    return decoded_token


def _validate_scopes(resource, decoded_token):
    token_scopes = decoded_token.get('scope', '').split(' ')

    # Validate against scopes registered in resource.
    # If a resource does not have at least one scope, it doesn't have any access restrictions.
    allowed_scopes = getattr(resource, 'auth', {}).get('allowed_scopes', [])
    if allowed_scopes and not set(allowed_scopes).issubset(token_scopes):
        raise falcon.HTTPForbidden(description='Check your permissions to access this resource.')
