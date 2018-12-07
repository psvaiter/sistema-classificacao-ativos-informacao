import falcon

from knoweak.api import constants
from knoweak.api.errors import Message, build_error
from knoweak.api.extensions import HTTPUnprocessableEntity
from knoweak.api.utils import get_collection_page, validate_str, patch_item
from knoweak.db import Session
from knoweak.db.models.catalog import BusinessDepartment


class Collection:
    """GET and POST departments in catalog."""

    def on_get(self, req, resp):
        """GETs a paged collection of departments available.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        """
        session = Session()
        try:
            query = session.query(BusinessDepartment).order_by(BusinessDepartment.name)

            data, paging = get_collection_page(req, query)
            resp.media = {
                'data': data,
                'paging': paging
            }
        finally:
            session.close()

    def on_post(self, req, resp):
        """Creates a new department in catalog.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        """
        session = Session()
        try:
            errors = validate_post(req.media, session)
            if errors:
                raise HTTPUnprocessableEntity(errors)

            # Copy fields from request to a BusinessDepartment object
            item = BusinessDepartment().fromdict(req.media, only=['name'])

            session.add(item)
            session.commit()
            resp.status = falcon.HTTP_CREATED
            resp.location = req.relative_uri + f'/{item.id}'
            resp.media = {'data': item.asdict()}
        finally:
            session.close()


class Item:
    """GET and PATCH a department in catalog."""

    def on_get(self, req, resp, department_id):
        """GETs a single department by id.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        :param department_id: The id of department to retrieve.
        """
        session = Session()
        try:
            item = session.query(BusinessDepartment).get(department_id)
            if item is None:
                raise falcon.HTTPNotFound()

            resp.media = {'data': item.asdict()}
        finally:
            session.close()

    def on_patch(self, req, resp, department_id):
        """Updates (partially) the department requested.
        All entities that reference the department will be affected by the update.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        :param department_id: The id of department to be patched.
        """
        session = Session()
        try:
            department = session.query(BusinessDepartment).get(department_id)
            if department is None:
                raise falcon.HTTPNotFound()

            errors = validate_patch(req.media, session)
            if errors:
                raise HTTPUnprocessableEntity(errors)

            patch_item(department, req.media, only=['name'])
            session.commit()

            resp.status = falcon.HTTP_OK
            resp.media = {'data': department.asdict()}
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
        return session.query(BusinessDepartment.name) \
            .filter(BusinessDepartment.name == name) \
            .first()
    return exists
