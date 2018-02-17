import falcon
from datetime import datetime

import app_constants as constants
from .extensions import HTTPUnprocessableEntity
from .utils import get_collection_page
from errors import Message, build_error
from models import Session, BusinessDepartment


class Collection:
    """GET and POST departments."""

    def on_get(self, req, resp):
        """GETs a paged collection of departments.

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
        """Creates a new department.

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

            session.add(item)
            session.commit()
            resp.status = falcon.HTTP_CREATED
            resp.media = {'data': item.asdict()}
        finally:
            session.close()


class Item:
    """GET and PATCH an organization."""

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
        """Updates (partially) the department.

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
    if not request_media:
        errors.append(build_error(Message.ERR_NO_CONTENT))
        return errors

    # Name is mandatory and must be unique. Validate length.
    name = request_media.get('name')
    if name is None:
        errors.append(build_error(Message.ERR_NAME_CANNOT_BE_NULL))
    elif len(name) > constants.GENERAL_NAME_MAX_LENGTH:
        errors.append(build_error(Message.ERR_NAME_MAX_LENGTH))
    elif session.query(BusinessDepartment.name)\
            .filter(BusinessDepartment.name == name)\
            .first():
        errors.append(build_error(Message.ERR_NAME_ALREADY_EXISTS))

    return errors


def validate_patch(request_media, session):
    errors = []
    if not request_media:
        errors.append(build_error(Message.ERR_NO_CONTENT))
        return errors

    # Validate name if informed
    if 'name' in request_media:
        name = request_media.get('name')

        # Cannot be null if informed
        if name is None:
            errors.append(build_error(Message.ERR_NAME_CANNOT_BE_NULL))

        # Length must be valid
        elif len(name) > constants.GENERAL_NAME_MAX_LENGTH:
            errors.append(build_error(Message.ERR_NAME_MAX_LENGTH))

        # Must be unique
        elif session.query(BusinessDepartment.name) \
                .filter(BusinessDepartment.name == name) \
                .first():
            errors.append(build_error(Message.ERR_NAME_ALREADY_EXISTS))

    return errors
