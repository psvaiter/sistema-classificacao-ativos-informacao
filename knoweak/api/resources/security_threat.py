import falcon

from knoweak.api import constants as constants
from knoweak.api.errors import Message, build_error
from knoweak.api.extensions import HTTPUnprocessableEntity
from knoweak.api.middlewares.auth import check_scope
from knoweak.api.utils import get_collection_page, validate_str, patch_item
from knoweak.db import Session
from knoweak.db.models.catalog import SecurityThreat


class Collection:
    """GET and POST security threats in catalog."""

    @falcon.before(check_scope, 'read:catalog')
    def on_get(self, req, resp):
        """GETs a paged collection of security threats available.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        """
        session = Session()
        try:
            query = session.query(SecurityThreat).order_by(SecurityThreat.name)

            data, paging = get_collection_page(req, query)
            resp.media = {
                'data': data,
                'paging': paging
            }
        finally:
            session.close()

    @falcon.before(check_scope, 'create:catalog')
    def on_post(self, req, resp):
        """Creates a new security threat in catalog.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        """
        session = Session()
        try:
            errors = validate_post(req.media, session)
            if errors:
                raise HTTPUnprocessableEntity(errors)

            # Copy fields from request to a SecurityThreat object
            item = SecurityThreat().fromdict(req.media, only=['name', 'description'])

            session.add(item)
            session.commit()
            resp.status = falcon.HTTP_CREATED
            resp.location = req.relative_uri + f'/{item.id}'
            resp.media = {'data': item.asdict()}
        finally:
            session.close()


class Item:
    """GET and PATCH a security threat in catalog."""

    @falcon.before(check_scope, 'read:catalog')
    def on_get(self, req, resp, security_threat_id):
        """GETs a single security threat by id.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        :param security_threat_id: The id of security threat to retrieve.
        """
        session = Session()
        try:
            item = session.query(SecurityThreat).get(security_threat_id)
            if item is None:
                raise falcon.HTTPNotFound()

            resp.media = {'data': item.asdict()}
        finally:
            session.close()

    @falcon.before(check_scope, 'update:catalog')
    def on_patch(self, req, resp, security_threat_id):
        """Updates (partially) the security threat requested.
        All entities that reference the security threat will be affected by the update.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        :param security_threat_id: The id of security threat to be patched.
        """
        session = Session()
        try:
            security_threat = session.query(SecurityThreat).get(security_threat_id)
            if security_threat is None:
                raise falcon.HTTPNotFound()

            errors = validate_patch(req.media, session)
            if errors:
                raise HTTPUnprocessableEntity(errors)

            patch_item(security_threat, req.media, only=['name', 'description'])
            session.commit()

            resp.status = falcon.HTTP_OK
            resp.media = {'data': security_threat.asdict()}
        finally:
            session.close()


def validate_post(request_media, session):
    errors = []

    # Validate name
    # -----------------------------------------------------
    name = request_media.get('name')
    error = validate_str('name', name,
                         is_mandatory=True,
                         max_length=constants.GENERAL_NAME_MAX_LENGTH,
                         exists_strategy=exists_name(name, session))
    if error:
        errors.append(error)

    # Validate description
    # -----------------------------------------------------
    description = request_media.get('description')
    error = validate_str('description', description, max_length=constants.GENERAL_DESCRIPTION_MAX_LENGTH)
    if error:
        errors.append(error)

    return errors


def validate_patch(request_media, session):
    errors = []

    if not request_media:
        errors.append(build_error(Message.ERR_NO_CONTENT))
        return errors

    # Validate name if informed
    # -----------------------------------------------------
    if 'name' in request_media:
        name = request_media.get('name')
        error = validate_str('name', name,
                             is_mandatory=True,
                             max_length=constants.GENERAL_NAME_MAX_LENGTH,
                             exists_strategy=exists_name(name, session))
        if error:
            errors.append(error)

    # Validate name if informed
    # -----------------------------------------------------
    if 'description' in request_media:
        description = request_media.get('description')
        error = validate_str('description', description, max_length=constants.GENERAL_DESCRIPTION_MAX_LENGTH)
        if error:
            errors.append(error)

    return errors


def exists_name(name, session):
    def exists():
        return session.query(SecurityThreat.name) \
            .filter(SecurityThreat.name == name) \
            .first()
    return exists
