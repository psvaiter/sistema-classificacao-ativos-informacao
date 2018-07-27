import knoweak


class AppInfo:

    def on_get(self, req, resp):
        resp.media = {
            'version': knoweak.__version__
        }
