import falcon
import app_setup
from wsgiref import simple_server

# Some WSGI servers expect the WSGI application to be named 'application' by default.
# Then we defined 'api' as a shorter option.
api = application = falcon.API()

app_setup.configure_media_handlers(api)
app_setup.configure_routes(api)

if __name__ == '__main__':

    # Use this server as the last resort, even for debugging because it's very (very) slow.
    # As a Windows alternative, run in terminal:
    #   > waitress-serve --port=8000 app:api
    # As a Linux alternative, run in terminal:
    #   > gunicorn --reload api

    host = ''
    port = 8000
    with simple_server.make_server(host, port, api) as httpd:
        print('Serving on port {}...'.format(port))
        httpd.serve_forever()
