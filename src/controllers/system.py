import falcon


class AppInfo:

    def on_get(self, req, resp):
        resp.media = {
            'version': '1.0.0-beta'
        }
