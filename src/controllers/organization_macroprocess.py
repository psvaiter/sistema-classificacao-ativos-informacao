import falcon
from .extensions import HTTPUnprocessableEntity
from .utils import get_collection_page
from errors import Message, build_error
from models import Session, OrganizationMacroprocess, Organization, BusinessMacroprocess, OrganizationDepartment


class Collection:
    """GET and POST macroprocesses of an organization."""

    def on_get(self, req, resp, organization_code):
        """GETs a paged collection of macroprocesses of an organization.

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
                .query(OrganizationMacroprocess) \
                .filter(OrganizationMacroprocess.organization_id == organization_code)\
                .order_by(OrganizationMacroprocess.created_on)

            data, paging = get_collection_page(req, query, custom_asdict)
            resp.media = {
                'data': data,
                'paging': paging
            }
        finally:
            session.close()

    def on_post(self, req, resp, organization_code):
        """Adds a macroprocess to an organization.

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

            item = OrganizationMacroprocess()
            item.organization_id = organization_code
            item.department_id = req.media['department_id']
            item.macroprocess_id = req.media['macroprocess_id']
            session.add(item)
            session.commit()

            resp.status = falcon.HTTP_CREATED
            resp.media = {'data': custom_asdict(item)}
        finally:
            session.close()


class Item:
    """GET and DELETE an organization macroprocess instance."""

    def on_get(self, req, resp, organization_code, macroprocess_instance_id):
        """GETs a single macroprocess of an organization department.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        :param organization_code: The code of the organization.
        :param macroprocess_instance_id: The id of the macroprocess instance to retrieve.
        """
        session = Session()
        try:
            item = session\
                .query(OrganizationMacroprocess)\
                .filter(OrganizationMacroprocess.instance_id == macroprocess_instance_id) \
                .filter(Organization.id == organization_code) \
                .first()
            if item is None:
                raise falcon.HTTPNotFound()

            resp.media = {'data': custom_asdict(item)}
        finally:
            session.close()

    def on_delete(self, req, resp, organization_code, macroprocess_instance_id):
        """Removes a macroprocess from an organization department.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        :param organization_code: The code of the organization.
        :param macroprocess_instance_id: The id of the macroprocess instance to be removed.
        """
        session = Session()
        try:
            item = session \
                .query(OrganizationMacroprocess) \
                .filter(OrganizationMacroprocess.instance_id == macroprocess_instance_id) \
                .filter(Organization.id == organization_code) \
                .first()
            if item is None:
                raise falcon.HTTPNotFound()

            session.delete(item)
            session.commit()
        finally:
            session.close()


def validate_post(request_media, organization_code, session):
    errors = []

    # Validate department id in organization
    # -----------------------------------------------------
    department_id = request_media.get('department_id')
    if department_id is None:
        errors.append(build_error(Message.ERR_FIELD_CANNOT_BE_NULL, field_name='departmentId'))
    elif not find_organization_department(department_id, organization_code, session):
        errors.append(build_error(Message.ERR_DEPARTMENT_ID_INVALID, field_name='departmentId'))

    # Validate macroprocess id and if it's already in department
    # -----------------------------------------------------
    macroprocess_id = request_media.get('macroprocess_id')
    if macroprocess_id is None:
        errors.append(build_error(Message.ERR_FIELD_CANNOT_BE_NULL, field_name='macroprocessId'))
    elif not session.query(BusinessMacroprocess).get(macroprocess_id):
        errors.append(build_error(Message.ERR_FIELD_VALUE_INVALID, field_name='macroprocessId'))
    elif find_organization_macroprocess(macroprocess_id, department_id, organization_code, session):
        errors.append(build_error(Message.ERR_FIELD_VALUE_ALREADY_EXISTS, field_name='departmentId/macroprocessId'))

    return errors


def find_organization_department(department_id, organization_code, session):
    query = session \
        .query(OrganizationDepartment)\
        .filter(OrganizationDepartment.organization_id == organization_code,
                OrganizationDepartment.department_id == department_id)

    return query.first()


def find_organization_macroprocess(macroprocess_id, department_id, organization_code, session):
    query = session \
        .query(OrganizationMacroprocess)\
        .filter(OrganizationDepartment.organization_id == organization_code,
                OrganizationDepartment.department_id == department_id,
                OrganizationMacroprocess.macroprocess_id == macroprocess_id)

    return query.first()


def custom_asdict(dictable_model):
    exclude = ['organization_id', 'department_id', 'macroprocess_id']
    include = {
        'department': {'only': ['id', 'name']},
        'macroprocess': {'only': ['id', 'name']}
    }
    return dictable_model.asdict(follow=include, exclude=exclude)
