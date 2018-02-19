import falcon
from datetime import datetime

import app_constants as constants
from .extensions import HTTPUnprocessableEntity
from .utils import get_collection_page, validate_str
from errors import Message, build_error
from models import Session, BusinessDepartment


class Collection:
    """GET and POST departments in catalog."""

    def on_get(self, req, resp):
        """GETs a paged collection of departments available.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        """
        session = Session()
        query = session.query(BusinessDepartment).order_by(BusinessDepartment.created_on)

        data, paging = get_collection_page(req, query)
        resp.media = {
            'data': data,
            'paging': paging
        }

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
            item = BusinessDepartment().fromdict(req.media)
            item.name = item.name.strip()

            session.add(item)
            session.commit()
            resp.status = falcon.HTTP_CREATED
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
        item = session.query(BusinessDepartment).get(department_id)
        if item is None:
            raise falcon.HTTPNotFound()

        resp.media = {'data': item.asdict()}

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

            # Apply fields informed in request, compare before and after
            # and save patch only if record has changed.
            old_department = department.asdict()
            department.fromdict(req.media, only=['name'])
            department.name = department.name.strip()
            new_department = department.asdict()
            if new_department != old_department:
                department.last_modified_on = datetime.utcnow()
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
