import falcon
from .extensions import HTTPUnprocessableEntity
from .utils import get_collection_page, patch_item
from errors import Message, build_error
from models import Session, OrganizationProcess, Organization, BusinessProcess, OrganizationMacroprocess, RatingLevel


class Collection:
    """GET and POST processes of an organization."""

    def on_get(self, req, resp, organization_code):
        """GETs a paged collection of processes of an organization.

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
                .query(OrganizationProcess) \
                .filter(OrganizationProcess.organization_id == organization_code)\
                .order_by(OrganizationProcess.created_on)

            data, paging = get_collection_page(req, query, custom_asdict)
            resp.media = {
                'data': data,
                'paging': paging
            }
        finally:
            session.close()

    def on_post(self, req, resp, organization_code):
        """Adds a process to an organization's macroprocess.

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

            item = OrganizationProcess()
            item.organization_id = organization_code
            item.macroprocess_instance_id = req.media['macroprocess_instance_id']
            item.process_id = req.media['process_id']
            session.add(item)
            session.commit()

            resp.status = falcon.HTTP_CREATED
            resp.media = {'data': custom_asdict(item)}
        finally:
            session.close()


class Item:
    """GET, PATCH and DELETE an organization's process instance."""

    def on_get(self, req, resp, organization_code, process_instance_id):
        """GETs a single instance of process of an organization.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        :param organization_code: The code of the organization.
        :param process_instance_id: The id of the process instance to retrieve.
        """
        session = Session()
        try:
            item = find_process_instance(process_instance_id, organization_code, session)
            if item is None:
                raise falcon.HTTPNotFound()

            resp.media = {'data': custom_asdict(item)}
        finally:
            session.close()

    def on_patch(self, req, resp, organization_code, process_instance_id):
        """Updates (partially) the process instance requested.
        All entities that reference the process instance will be affected by the update.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        :param organization_code: The code of organization containing the process.
        :param process_instance_id: The id of process instance to be patched.
        """
        session = Session()
        try:
            process_instance = find_process_instance(process_instance_id, organization_code, session)
            if process_instance is None:
                raise falcon.HTTPNotFound()

            errors = validate_patch(req.media, organization_code, session)
            if errors:
                raise HTTPUnprocessableEntity(errors)

            patch_item(process_instance, req.media, only=['relevance_level_id'])
            session.commit()

            resp.status = falcon.HTTP_OK
            resp.media = {'data': custom_asdict(process_instance)}
        finally:
            session.close()

    def on_delete(self, req, resp, organization_code, process_instance_id):
        """Removes a process from an organization's macroprocess instance.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        :param organization_code: The code of the organization.
        :param process_instance_id: The id of the process instance to be removed.
        """
        session = Session()
        try:
            item = find_process_instance(process_instance_id, organization_code, session)
            if item is None:
                raise falcon.HTTPNotFound()

            session.delete(item)
            session.commit()
        finally:
            session.close()


def validate_post(request_media, organization_code, session):
    errors = []

    # Validate macroprocess instance id
    # -----------------------------------------------------
    macroprocess_instance_id = request_media.get('macroprocess_instance_id')
    if macroprocess_instance_id is None:
        errors.append(build_error(Message.ERR_FIELD_CANNOT_BE_NULL, field_name='macroprocessInstanceId'))
    elif not find_organization_macroprocess(macroprocess_instance_id, session):
        errors.append(build_error(Message.ERR_FIELD_VALUE_INVALID, field_name='macroprocessInstanceId'))

    # Validate process id and if it's already in organization macroprocess
    # -----------------------------------------------------
    process_id = request_media.get('process_id')
    if process_id is None:
        errors.append(build_error(Message.ERR_FIELD_CANNOT_BE_NULL, field_name='processId'))
    elif not session.query(BusinessProcess).get(process_id):
        errors.append(build_error(Message.ERR_FIELD_VALUE_INVALID, field_name='processId'))
    elif find_organization_process(process_id, macroprocess_instance_id, organization_code, session):
        errors.append(build_error(Message.ERR_FIELD_VALUE_ALREADY_EXISTS, field_name='macroprocessInstanceId/processId'))

    return errors


def validate_patch(request_media, organization_code, session):
    errors = []

    if not request_media:
        errors.append(build_error(Message.ERR_NO_CONTENT))
        return errors

    # Validate relevance level id if informed
    # -----------------------------------------------------
    if 'relevance_level_id' in request_media:
        relevance_level_id = request_media.get('relevance_level_id')

        # This value CAN be null if informed...
        if relevance_level_id and not session.query(RatingLevel).get(relevance_level_id):
            errors.append(build_error(Message.ERR_FIELD_VALUE_INVALID, field_name='relevanceLevelId'))

    return errors


def find_organization_macroprocess(macroprocess_instance_id, session):
    query = session \
        .query(OrganizationMacroprocess) \
        .filter(OrganizationMacroprocess.instance_id == macroprocess_instance_id)

    return query.first()


def find_organization_process(process_id, macroprocess_instance_id, organization_id, session):
    query = session \
        .query(OrganizationProcess) \
        .filter(OrganizationProcess.organization_id == organization_id,
                OrganizationProcess.macroprocess_instance_id == macroprocess_instance_id,
                OrganizationProcess.process_id == process_id)

    return query.first()


def find_process_instance(process_instance_id, organization_id, session):
    query = session \
        .query(OrganizationProcess) \
        .filter(OrganizationProcess.instance_id == process_instance_id) \
        .filter(Organization.id == organization_id)

    return query.first()


def custom_asdict(dictable_model):
    exclude = ['organization_id', 'process_id']
    include = {
        'process': {'only': ['id', 'name']}
    }
    return dictable_model.asdict(follow=include, exclude=exclude)
