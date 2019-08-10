from knoweak.setup import get_api
from wsgiref import simple_server

# Some WSGI servers expect the WSGI application to be named 'application'
# by default. Then we defined 'api' as a shorter option too.
api = application = get_api()

if __name__ == '__main__':

    # Use this simple server as the last resort, even for debugging
    # because it's very (very) slow.
    # In Windows, run in terminal:
    #   > waitress-serve --port=8000 app:api
    # In Linux, run in terminal:
    #   > gunicorn --reload api

    host = ''
    port = 8000
    with simple_server.make_server(host, port, api) as httpd:
        print('Serving on port {}...'.format(port))
        httpd.serve_forever()
