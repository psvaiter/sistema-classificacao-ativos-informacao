import falcon
from sqlalchemy.orm import joinedload

from knoweak.errors import Message, build_error
from .extensions import HTTPUnprocessableEntity
from .utils import get_collection_page
from ..models import Session, OrganizationDepartment, Organization, BusinessDepartment


class Collection:
    """GET and POST departments of an organization."""

    def on_get(self, req, resp, organization_code):
        """GETs a paged collection of departments of an organization.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        :param organization_code: The code of the organization.
        """
        session = Session()
        try:
            organization = session.query(Organization).get(organization_code)
            if organization is None:
                raise falcon.HTTPNotFound()

            # Build query to fetch items
            query = session\
                .query(OrganizationDepartment)\
                .filter(OrganizationDepartment.organization_id == organization_code)\
                .order_by(OrganizationDepartment.created_on)\
                .options(joinedload(OrganizationDepartment.department, innerjoin=True))

            data, paging = get_collection_page(req, query, custom_asdict)
            resp.media = {
                'data': data,
                'paging': paging
            }
        finally:
            session.close()

    def on_post(self, req, resp, organization_code):
        """Adds a department to an organization.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        :param organization_code: The code of the organization.
        """
        session = Session()
        try:
            organization = session.query(Organization).get(organization_code)
            if organization is None:
                raise falcon.HTTPNotFound()

            errors = validate_post(req.media, organization_code, session)
            if errors:
                raise HTTPUnprocessableEntity(errors)

            item = OrganizationDepartment()
            item.organization_id = organization_code
            item.department_id = req.media['id']
            session.add(item)
            session.commit()

            resp.status = falcon.HTTP_CREATED
            resp.location = req.relative_uri + f'/{item.department_id}'
            resp.media = {'data': custom_asdict(item)}
        finally:
            session.close()


class Item:
    """GET and DELETE an organization department."""

    def on_get(self, req, resp, organization_code, department_id):
        """GETs a single department of an organization.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        :param organization_code: The code of the organization.
        :param department_id: The id of department to retrieve.
        """
        session = Session()
        try:
            item = find_organization_department(department_id, organization_code, session)
            if item is None:
                raise falcon.HTTPNotFound()

            resp.media = {'data': custom_asdict(item)}
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


def validate_post(request_media, organization_code, session):
    errors = []

    # Validate department id
    # -----------------------------------------------------
    department_id = request_media.get('id')
    if department_id is None:
        errors.append(build_error(Message.ERR_DEPARTMENT_ID_CANNOT_BE_NULL, field_name='id'))
    elif not session.query(BusinessDepartment).get(department_id):
        errors.append(build_error(Message.ERR_DEPARTMENT_ID_INVALID, field_name='id'))

    # Validate department in organization
    # -----------------------------------------------------
    elif find_organization_department(department_id, organization_code, session):
        errors.append(build_error(Message.ERR_DEPARTMENT_ID_ALREADY_IN_ORGANIZATION, field_name='id'))

    return errors


def find_organization_department(department_id, organization_code, session):
    query = session \
        .query(OrganizationDepartment)\
        .filter(OrganizationDepartment.organization_id == organization_code,
                OrganizationDepartment.department_id == department_id)

    return query.first()


def custom_asdict(dictable_model):
    follow = {'department': {'only': ['id', 'name']}}
    return dictable_model.asdict(follow=follow, exclude=['department_id'])
