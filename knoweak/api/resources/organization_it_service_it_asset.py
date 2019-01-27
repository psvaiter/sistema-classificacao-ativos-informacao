import falcon

from knoweak.api.errors import build_error, Message
from knoweak.api.extensions import HTTPUnprocessableEntity
from knoweak.api.middlewares.auth import check_scope
from knoweak.api.utils import get_collection_page, patch_item
from knoweak.db import Session
from knoweak.db.models.organization import OrganizationITServiceITAsset, OrganizationITService, OrganizationITAsset
from knoweak.db.models.system import RatingLevel


class Collection:
    """GET and POST instances of IT assets from/into an organization's IT service."""

    @falcon.before(check_scope, 'read:organizations')
    def on_get(self, req, resp, organization_code, it_service_instance_id):
        """ GETs a paged collection of IT assets in an organization IT service.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        :param organization_code: The code of the organization.
        :param it_service_instance_id: The id of the IT service instance.
        """
        session = Session()
        try:
            it_service_instance = find_it_service_instance(it_service_instance_id, organization_code, session)
            if it_service_instance is None:
                raise falcon.HTTPNotFound()

            # Build query to fetch items
            query = session \
                .query(OrganizationITServiceITAsset) \
                .join(OrganizationITService) \
                .filter(OrganizationITService.organization_id == organization_code) \
                .filter(OrganizationITService.instance_id == it_service_instance_id) \
                .order_by(OrganizationITServiceITAsset.created_on)

            data, paging = get_collection_page(req, query, custom_asdict)
            resp.media = {
                'data': data,
                'paging': paging
            }
        finally:
            session.close()

    @falcon.before(check_scope, 'manage:organizations')
    def on_post(self, req, resp, organization_code, it_service_instance_id):
        """Adds an instance of IT asset to an organization IT service.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        :param organization_code: The code of the organization.
        :param it_service_instance_id: The id of the IT service instance.
        """
        session = Session()
        try:
            it_service_instance = find_it_service_instance(it_service_instance_id, organization_code, session)
            if it_service_instance is None:
                raise falcon.HTTPNotFound()

            errors = validate_post(req.media, organization_code, it_service_instance_id, session)
            if errors:
                raise HTTPUnprocessableEntity(errors)

            accepted_fields = ['it_asset_instance_id', 'relevance_level_id']
            item = OrganizationITServiceITAsset().fromdict(req.media, only=accepted_fields)
            item.it_service_instance = it_service_instance
            session.add(item)
            session.commit()

            resp.status = falcon.HTTP_CREATED
            resp.location = req.relative_uri + f'/{item.it_asset_instance_id}'
            resp.media = {'data': custom_asdict(item)}
        finally:
            session.close()


class Item:
    """PATCH and DELETE an IT asset of/from an organization's IT service instance."""

    @falcon.before(check_scope, 'manage:organizations')
    def on_patch(self, req, resp, organization_code, it_service_instance_id, it_asset_instance_id):
        """Updates (partially) the relationship IT service-IT asset requested.
        All entities that reference the relationship will be affected by the update.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        :param organization_code: The code of the organization.
        :param it_service_instance_id: The id of the IT service instance to be patched.
        :param it_asset_instance_id: The id of the IT asset instance to be patched.
        """
        session = Session()
        try:
            # Route params are checked in two steps:
            # 1st step: check if IT service is in organization
            # 2nd step: check if IT asset is in organization IT service
            it_service_instance = find_it_service_instance(it_service_instance_id, organization_code, session)
            it_service_asset = find_it_service_it_asset(it_asset_instance_id, it_service_instance_id, session)
            if it_service_instance is None or it_service_asset is None:
                raise falcon.HTTPNotFound()

            errors = validate_patch(req.media, organization_code, session)
            if errors:
                raise HTTPUnprocessableEntity(errors)

            patch_item(it_service_asset, req.media, only=['relevance_level_id'])
            session.commit()

            resp.status = falcon.HTTP_OK
            resp.media = {'data': custom_asdict(it_service_asset)}
        finally:
            session.close()

    @falcon.before(check_scope, 'manage:organizations')
    def on_delete(self, req, resp, organization_code, it_service_instance_id, it_asset_instance_id):
        """Removes an instance of IT asset from an organization IT service.
        It doesn't remove the IT asset from the organization.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        :param organization_code: The code of the organization.
        :param it_service_instance_id: The id of the IT service instance from which the IT asset should be removed.
        :param it_asset_instance_id: The id of the IT asset instance to be removed.
        """
        session = Session()
        try:
            # Route params are checked in two steps:
            # 1st step: check if IT service is in organization
            # 2nd step: check if IT asset is in organization IT service
            it_service_instance = find_it_service_instance(it_service_instance_id, organization_code, session)
            it_service_asset = find_it_service_it_asset(it_asset_instance_id, it_service_instance_id, session)
            if it_service_instance is None or it_service_asset is None:
                raise falcon.HTTPNotFound()

            session.delete(it_service_asset)
            session.commit()
        finally:
            session.close()


def validate_post(request_media, organization_code, it_service_instance_id, session):
    errors = []

    # Validate IT asset instance id
    # It MUST exist in organization and MUST NOT already exist in organization IT service
    # -----------------------------------------------------
    it_asset_instance_id = request_media.get('it_asset_instance_id')
    if it_asset_instance_id is None:
        errors.append(build_error(Message.ERR_FIELD_CANNOT_BE_NULL, field_name='itAssetInstanceId'))
    elif not find_it_asset_in_organization(it_asset_instance_id, organization_code, session):
        errors.append(build_error(Message.ERR_FIELD_VALUE_INVALID, field_name='itAssetInstanceId'))
    elif find_it_service_it_asset(it_asset_instance_id, it_service_instance_id, session):
        errors.append(build_error(Message.ERR_FIELD_VALUE_ALREADY_EXISTS, field_name='itServiceInstanceId/itAssetInstanceId'))

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


def find_it_service_instance(it_service_instance_id, organization_code, session):
    query = session \
        .query(OrganizationITService) \
        .filter(OrganizationITService.organization_id == organization_code) \
        .filter(OrganizationITService.instance_id == it_service_instance_id)
    return query.first()


def find_it_asset_in_organization(it_asset_instance_id, organization_code, session):
    query = session \
        .query(OrganizationITAsset) \
        .filter(OrganizationITAsset.organization_id == organization_code) \
        .filter(OrganizationITAsset.instance_id == it_asset_instance_id)
    return query.first()


def find_it_service_it_asset(it_asset_instance_id, it_service_instance_id, session):
    return session \
        .query(OrganizationITServiceITAsset) \
        .get((it_service_instance_id, it_asset_instance_id))


def custom_asdict(dictable_model):
    exclude = None
    follow = {
        'it_asset_instance': {'only': ['external_identifier'], 'follow': {
            'it_asset': {'only': ['id', 'name']}
        }}
    }
    return dictable_model.asdict(follow=follow, exclude=exclude)
