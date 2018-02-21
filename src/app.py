import falcon
import app_setup as setup
# from wsgiref.simple_server import make_server


api = application = falcon.API()

setup.configure_media_handlers(api)
setup.configure_routes(api)

# if __name__ == '__main__':
#     httpd = make_server('', 8000, api)
#     print('Serving on port 8000...')
#
#     httpd.serve_forever()
