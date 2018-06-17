import falcon
import app_constants as constants
from .extensions import HTTPUnprocessableEntity
from .utils import get_collection_page, validate_str, patch_item, validate_number
from errors import Message, build_error
from models import Session, SystemAdministrativeRole


class Collection:
    """GET and POST system roles."""

    def on_get(self, req, resp):
        """GETs a paged collection of system roles.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        """
        session = Session()
        try:
            query = session.query(SystemAdministrativeRole).order_by(SystemAdministrativeRole.created_on)

            data, paging = get_collection_page(req, query)
            resp.media = {
                'data': data,
                'paging': paging
            }
        finally:
            session.close()

    def on_post(self, req, resp):
        """Creates a new system role.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        """
        session = Session()
        try:
            errors = validate_post(req.media, session)
            if errors:
                raise HTTPUnprocessableEntity(errors)

            # Copy fields from request to a SystemAdministrativeRole object
            item = SystemAdministrativeRole().fromdict(req.media, only=['id', 'name', 'description'])

            session.add(item)
            session.commit()
            resp.status = falcon.HTTP_CREATED
            resp.location = req.relative_uri + f'/{item.id}'
            resp.media = {'data': item.asdict()}
        finally:
            session.close()


class Item:
    """GET and PATCH a system role."""

    def on_get(self, req, resp, role_id):
        """GETs a single role by id.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        :param role_id: The id of role to retrieve.
        """
        session = Session()
        try:
            item = session.query(SystemAdministrativeRole).get(role_id)
            if item is None:
                raise falcon.HTTPNotFound()

            resp.media = {'data': item.asdict()}
        finally:
            session.close()

    def on_patch(self, req, resp, role_id):
        """Updates (partially) the system role requested.
        All entities that reference the system role will be affected by the update.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        :param role_id: The id of role to be patched.
        """
        session = Session()
        try:
            item = session.query(SystemAdministrativeRole).get(role_id)
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

    # Validate id
    # -----------------------------------------------------
    role_id = request_media.get('id')
    error = validate_number('id', role_id,
                            is_mandatory=True,
                            min_value=1,
                            exists_strategy=exists_role_id(role_id, session))
    if error:
        errors.append(error)

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

    # Validate description if informed
    # -----------------------------------------------------
    if 'description' in request_media:
        description = request_media.get('description')
        error = validate_str('description', description, max_length=constants.GENERAL_DESCRIPTION_MAX_LENGTH)
        if error:
            errors.append(error)

    return errors


def exists_role_id(role_id, session):
    def exists():
        return session.query(SystemAdministrativeRole.id) \
            .filter(SystemAdministrativeRole.id == role_id) \
            .first()
    return exists


def exists_name(name, session):
    def exists():
        return session.query(SystemAdministrativeRole.name) \
            .filter(SystemAdministrativeRole.name == name) \
            .first()
    return exists
