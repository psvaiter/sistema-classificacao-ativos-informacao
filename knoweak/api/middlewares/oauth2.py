import falcon
import jwt

from knoweak.settings import AUTH


class OAuth2:

    def __init__(self):
        pass

    def process_resource(self, req, resp, resource, params):
        if AUTH['disabled']:
            return

        auth_header = req.get_header('Authorization')
        if not auth_header:
            raise falcon.HTTPUnauthorized(description='Authorization header required.')

        auth_header_parts = auth_header.split(' ', 1)
        if not auth_header_parts[0] == 'Bearer':
            raise falcon.HTTPUnauthorized(description='Invalid authentication scheme. Expected value: Bearer.')
        if len(auth_header_parts) == 1:
            raise falcon.HTTPUnauthorized(description='Missing Bearer token.')

        try:
            decoded_token = jwt.decode(auth_header_parts[1], key='', algorithms='HS256')
        except Exception as e:
            raise falcon.HTTPUnauthorized(description=f'Invalid authentication token. {str(e)}.')

        self._validate_scopes(resource, decoded_token)

    def _validate_scopes(self, resource, decoded_token):
        # Read the scopes from token. It can be either a string or a list.
        token_scopes = decoded_token.get('scopes', [])
        if isinstance(token_scopes, str):
            token_scopes = token_scopes.split(' ')
        elif not isinstance(token_scopes, list):
            token_scopes = []

        # Validate against scopes registered in resource.
        # If a resource does not have at least one scope, it doesn't have any access restrictions.
        allowed_scopes = getattr(resource, 'auth', {}).get('allowed_scopes', [])
        if allowed_scopes and not set(allowed_scopes).issubset(token_scopes):
            raise falcon.HTTPForbidden(description='Check your permissions (scopes).')
