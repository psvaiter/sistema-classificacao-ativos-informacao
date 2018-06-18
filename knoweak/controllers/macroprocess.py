import falcon

from knoweak import app_constants as constants
from knoweak.errors import Message, build_error
from .extensions import HTTPUnprocessableEntity
from .utils import get_collection_page, validate_str, patch_item
from ..models import Session, BusinessMacroprocess


class Collection:
    """GET and POST macroprocesses in catalog."""

    def on_get(self, req, resp):
        """GETs a paged collection of macroprocesses available.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        """
        session = Session()
        try:
            query = session.query(BusinessMacroprocess).order_by(BusinessMacroprocess.created_on)

            data, paging = get_collection_page(req, query)
            resp.media = {
                'data': data,
                'paging': paging
            }
        finally:
            session.close()

    def on_post(self, req, resp):
        """Creates a new macroprocess in catalog.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        """
        session = Session()
        try:
            errors = validate_post(req.media, session)
            if errors:
                raise HTTPUnprocessableEntity(errors)

            # Copy fields from request to a BusinessMacroprocess object
            item = BusinessMacroprocess().fromdict(req.media, only=['name'])

            session.add(item)
            session.commit()
            resp.status = falcon.HTTP_CREATED
            resp.location = req.relative_uri + f'/{item.id}'
            resp.media = {'data': item.asdict()}
        finally:
            session.close()


class Item:
    """GET and PATCH a macroprocess in catalog."""

    def on_get(self, req, resp, macroprocess_id):
        """GETs a single macroprocess by id.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        :param macroprocess_id: The id of macroprocess to retrieve.
        """
        session = Session()
        try:
            item = session.query(BusinessMacroprocess).get(macroprocess_id)
            if item is None:
                raise falcon.HTTPNotFound()

            resp.media = {'data': item.asdict()}
        finally:
            session.close()

    def on_patch(self, req, resp, macroprocess_id):
        """Updates (partially) the macroprocess requested.
        All entities that reference the macroprocess will be affected by the update.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        :param macroprocess_id: The id of macroprocess to be patched.
        """
        session = Session()
        try:
            macroprocess = session.query(BusinessMacroprocess).get(macroprocess_id)
            if macroprocess is None:
                raise falcon.HTTPNotFound()

            errors = validate_patch(req.media, session)
            if errors:
                raise HTTPUnprocessableEntity(errors)

            patch_item(macroprocess, req.media, only=['name'])
            session.commit()

            resp.status = falcon.HTTP_OK
            resp.media = {'data': macroprocess.asdict()}
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

    return errors


def exists_name(name, session):
    def exists():
        return session.query(BusinessMacroprocess.name) \
            .filter(BusinessMacroprocess.name == name) \
            .first()
    return exists
