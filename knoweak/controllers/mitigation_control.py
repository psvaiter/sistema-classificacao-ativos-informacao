import falcon

from knoweak import app_constants as constants
from knoweak.errors import Message, build_error
from .extensions import HTTPUnprocessableEntity
from .utils import get_collection_page, validate_str, patch_item
from ..models import Session, MitigationControl


class Collection:
    """GET and POST mitigation controls in catalog."""

    def on_get(self, req, resp):
        """GETs a paged collection of mitigation controls available.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        """
        session = Session()
        try:
            query = session.query(MitigationControl).order_by(MitigationControl.created_on)

            data, paging = get_collection_page(req, query)
            resp.media = {
                'data': data,
                'paging': paging
            }
        finally:
            session.close()

    def on_post(self, req, resp):
        """Creates a new mitigation control in catalog.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        """
        session = Session()
        try:
            errors = validate_post(req.media, session)
            if errors:
                raise HTTPUnprocessableEntity(errors)

            # Copy fields from request to a MitigationControl object
            item = MitigationControl().fromdict(req.media, only=['name', 'description'])

            session.add(item)
            session.commit()
            resp.status = falcon.HTTP_CREATED
            resp.location = req.relative_uri + f'/{item.id}'
            resp.media = {'data': item.asdict()}
        finally:
            session.close()


class Item:
    """GET and PATCH a mitigation control in catalog."""

    def on_get(self, req, resp, mitigation_control_id):
        """GETs a single mitigation control by id.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        :param mitigation_control_id: The id of mitigation control to retrieve.
        """
        session = Session()
        try:
            item = session.query(MitigationControl).get(mitigation_control_id)
            if item is None:
                raise falcon.HTTPNotFound()

            resp.media = {'data': item.asdict()}
        finally:
            session.close()

    def on_patch(self, req, resp, mitigation_control_id):
        """Updates (partially) the mitigation control requested.
        All entities that reference the mitigation control will be affected by the update.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        :param mitigation_control_id: The id of mitigation control to be patched.
        """
        session = Session()
        try:
            item = session.query(MitigationControl).get(mitigation_control_id)
            if item is None:
                raise falcon.HTTPNotFound()

            errors = validate_patch(req.media, session)
            if errors:
                raise HTTPUnprocessableEntity(errors)

            patch_item(item, req.media, only=['name', 'description'])
            session.commit()

            resp.status = falcon.HTTP_OK
            resp.media = {'data': item.asdict()}
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
        return session.query(MitigationControl.name) \
            .filter(MitigationControl.name == name) \
            .first()
    return exists
