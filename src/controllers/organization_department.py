import falcon
from datetime import datetime

import app_constants as constants
from .extensions import HTTPUnprocessableEntity
from .utils import get_collection_page
from errors import Message, build_error
from models import Session, OrganizationDepartment, Organization, BusinessDepartment


class Collection:
    """GET departments of an organization."""

    def on_get(self, req, resp, organization_code):
        """GETs a paged collection of departments of an organization.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        :param organization_code: The code of the organization to get the departments.
        """
        session = Session()

        organization = session.query(Organization).get(organization_code)
        if organization is None:
            raise falcon.HTTPNotFound()

        query = session\
            .query(OrganizationDepartment)\
            .filter(Organization.organization_id == organization_code)\
            .order_by(OrganizationDepartment.created_on)

        data, paging = get_collection_page(req, query)
        resp.media = {
            'data': data,
            'paging': paging
        }


class Item:
    """GET, PUT and DELETE an organization department."""

    def on_get(self, req, resp, organization_code, department_id):
        """GETs a single department of an organization.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        :param organization_code: The code of the organization.
        :param department_id: The id of department to retrieve.
        """
        session = Session()
        item = find_organization_department(department_id, organization_code, session)
        if item is None:
            raise falcon.HTTPNotFound()

        resp.media = {'data': item.asdict()}

    def on_put(self, req, resp, organization_code, department_id):
        """Adds a department to an organization. Replaces the existing one
        if already exists.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        :param organization_code: The code of organization.
        :param department_id: The id of department being added.
        """
        session = Session()
        try:
            validate_put_item(organization_code, department_id, req.media, session)
            item = add_or_update(department_id, organization_code, session)
            session.commit()

            resp.status = falcon.HTTP_OK
            resp.media = {'data': item.asdict()}
        finally:
            session.close()

    def on_delete(self, req, resp, organization_code, department_id):
        """Removes a department from an organization.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        :param organization_code: The code of the organization.
        :param department_id: The id of the department to be removed.
        """
        session = Session()
        try:
            item = find_organization_department(department_id, organization_code, session)
            if item is None:
                raise falcon.HTTPNotFound()

            session.delete(item)
            session.commit()
        finally:
            session.close()


def validate_put_item(organization_code, department_id, request_media, session):
    errors = []

    # Check if organization exists (404)
    organization = session.query(Organization).get(organization_code)
    if organization is None:
        raise falcon.HTTPNotFound()

    # Check if department exists
    department = session.query(BusinessDepartment).get(department_id)
    if department is None:
        errors.append(build_error(Message.ERR_DEPARTMENT_ID_NOT_FOUND))

    # if not request_media:
    #     errors.append(build_error(Message.ERR_NO_CONTENT))
    #     return errors

    if errors:
        raise HTTPUnprocessableEntity(errors)


def add_or_update(organization_code, department_id, session):
    organization_department = find_organization_department(department_id, organization_code, session)

    # Add if doesn't exist
    if organization_department is None:
        organization_department = OrganizationDepartment(
            organization_id=organization_code,
            business_department_id=department_id
        )
        session.add(organization_department)

    return organization_department


def find_organization_department(department_id, organization_code, session):
    query = session \
        .query(OrganizationDepartment) \
        .filter(OrganizationDepartment.organization_id == organization_code,
                OrganizationDepartment.business_department_id == department_id) \

    return query.first()
