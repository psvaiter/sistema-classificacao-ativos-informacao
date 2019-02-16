import falcon
from sqlalchemy.exc import SQLAlchemyError

import knoweak
from knoweak.db import Session
from knoweak.db.models.system import RatingLevel


class AppInfo:

    def on_get(self, req, resp):
        resp.media = {
            'version': knoweak.__version__
        }


class HealthCheck:

    def on_get(self, req, resp):
        errors = []
        test_database(errors)

        if not errors:
            resp.status = falcon.HTTP_OK
            return

        resp.status = falcon.HTTP_MULTI_STATUS
        resp.media = {
            'components': errors
        }


def test_database(errors):
    try:
        session = Session()
        session.query(RatingLevel).first()
    except SQLAlchemyError:
        errors.append({
            'name': 'database',
            'status': falcon.HTTP_INTERNAL_SERVER_ERROR
        })
