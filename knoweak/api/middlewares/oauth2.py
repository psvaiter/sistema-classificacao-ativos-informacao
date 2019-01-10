import falcon
from knoweak.settings import AUTH


class OAuth2:

    def process_request(self, req, resp):
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
