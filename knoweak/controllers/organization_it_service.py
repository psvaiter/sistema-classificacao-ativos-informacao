import falcon

from knoweak.errors import Message, build_error
from .extensions import HTTPUnprocessableEntity
from .utils import get_collection_page, patch_item
from ..models import Session, OrganizationITService, Organization, ITService, OrganizationProcess, RatingLevel


class Collection:
    """GET and POST IT services of an organization."""

    def on_get(self, req, resp, organization_code):
        """GETs a paged collection of IT services of an organization.

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
                .query(OrganizationITService) \
                .filter(OrganizationITService.organization_id == organization_code)\
                .order_by(OrganizationITService.created_on)

            data, paging = get_collection_page(req, query, custom_asdict)
            resp.media = {
                'data': data,
                'paging': paging
            }
        finally:
            session.close()

    def on_post(self, req, resp, organization_code):
        """Adds a IT service to an organization's process.

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

            accepted_fields = ['process_instance_id', 'it_service_id', 'relevance_level_id']
            item = OrganizationITService().fromdict(req.media, only=accepted_fields)
            item.organization_id = organization_code
            session.add(item)
            session.commit()

            resp.status = falcon.HTTP_CREATED
            resp.location = req.relative_uri + f'/{item.instance_id}'
            resp.media = {'data': custom_asdict(item)}
        finally:
            session.close()


class Item:
    """GET, PATCH and DELETE an organization's IT service instance."""

    def on_get(self, req, resp, organization_code, it_service_instance_id):
        """GETs a single instance of IT service of an organization.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        :param organization_code: The code of the organization.
        :param it_service_instance_id: The id of the IT service instance to retrieve.
        """
        session = Session()
        try:
            item = find_it_service_instance(it_service_instance_id, organization_code, session)
            if item is None:
                raise falcon.HTTPNotFound()

            resp.media = {'data': custom_asdict(item)}
        finally:
            session.close()

    def on_patch(self, req, resp, organization_code, it_service_instance_id):
        """Updates (partially) the IT service instance requested.
        All entities that reference the IT service instance will be affected by the update.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        :param organization_code: The code of organization.
        :param it_service_instance_id: The id of IT service instance to be patched.
        """
        session = Session()
        try:
            process_instance = find_it_service_instance(it_service_instance_id, organization_code, session)
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

    def on_delete(self, req, resp, organization_code, it_service_instance_id):
        """Removes an IT service from an organization's process instance.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        :param organization_code: The code of the organization.
        :param it_service_instance_id: The id of the IT service instance to be removed.
        """
        session = Session()
        try:
            item = find_it_service_instance(it_service_instance_id, organization_code, session)
            if item is None:
                raise falcon.HTTPNotFound()

            session.delete(item)
            session.commit()
        finally:
            session.close()


def validate_post(request_media, organization_code, session):
    errors = []

    # Validate process instance id
    # -----------------------------------------------------
    process_instance_id = request_media.get('process_instance_id')
    if process_instance_id is None:
        errors.append(build_error(Message.ERR_FIELD_CANNOT_BE_NULL, field_name='processInstanceId'))
    elif not find_organization_process(process_instance_id, session):
        errors.append(build_error(Message.ERR_FIELD_VALUE_INVALID, field_name='processInstanceId'))

    # Validate IT service id and if it's already in organization process
    # -----------------------------------------------------
    it_service_id = request_media.get('it_service_id')
    if it_service_id is None:
        errors.append(build_error(Message.ERR_FIELD_CANNOT_BE_NULL, field_name='itServiceId'))
    elif not session.query(ITService).get(it_service_id):
        errors.append(build_error(Message.ERR_FIELD_VALUE_INVALID, field_name='itServiceId'))
    elif find_organization_it_service(it_service_id, process_instance_id, organization_code, session):
        errors.append(build_error(Message.ERR_FIELD_VALUE_ALREADY_EXISTS, field_name='processInstanceId/itServiceId'))

    # Validate relevance level if informed
    # -----------------------------------------------------
    relevance_level_id = request_media.get('relevance_level_id')
    if relevance_level_id and not session.query(RatingLevel).get(relevance_level_id):
        errors.append(build_error(Message.ERR_FIELD_VALUE_INVALID, field_name='relevanceLevelId'))

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


def find_organization_process(process_instance_id, session):
    query = session \
        .query(OrganizationProcess) \
        .filter(OrganizationProcess.instance_id == process_instance_id)

    return query.first()


def find_organization_it_service(it_service_id, process_instance_id, organization_id, session):
    query = session \
        .query(OrganizationITService) \
        .filter(OrganizationITService.organization_id == organization_id,
                OrganizationITService.process_instance_id == process_instance_id,
                OrganizationITService.it_service_id == it_service_id)

    return query.first()


def find_it_service_instance(it_service_instance_id, organization_id, session):
    query = session \
        .query(OrganizationITService) \
        .filter(OrganizationITService.instance_id == it_service_instance_id) \
        .filter(OrganizationITService.organization_id == organization_id)

    return query.first()


def custom_asdict(dictable_model):
    exclude = ['organization_id', 'it_service_id']
    include = {
        'it_service': {'only': ['id', 'name']}
    }
    return dictable_model.asdict(follow=include, exclude=exclude)
