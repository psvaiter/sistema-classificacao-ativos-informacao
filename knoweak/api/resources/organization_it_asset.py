import falcon
from sqlalchemy import func

from knoweak.api import constants as constants
from knoweak.api.errors import Message, build_error
from knoweak.api.extensions import HTTPUnprocessableEntity
from knoweak.api.middlewares.auth import check_scope
from knoweak.api.utils import get_collection_page, patch_item, validate_str
from knoweak.db import Session
from knoweak.db.models.catalog import ITAsset
from knoweak.db.models.organization import Organization, OrganizationITAsset


class Collection:
    """GET and POST IT assets of an organization."""

    @falcon.before(check_scope, 'read:organizations')
    def on_get(self, req, resp, organization_code):
        """GETs a paged collection of IT assets of an organization.

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
                .query(OrganizationITAsset)\
                .join(ITAsset)\
                .filter(OrganizationITAsset.organization_id == organization_code)\
                .order_by(ITAsset.name, OrganizationITAsset.external_identifier, OrganizationITAsset.created_on)

            data, paging = get_collection_page(req, query, custom_asdict)
            resp.media = {
                'data': data,
                'paging': paging
            }
        finally:
            session.close()

    @falcon.before(check_scope, 'manage:organizations')
    def on_post(self, req, resp, organization_code):
        """Adds a IT asset to an organization's IT service.

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

            accepted_fields = ['it_asset_id', 'external_identifier']
            item = OrganizationITAsset().fromdict(req.media, only=accepted_fields)
            item.organization_id = organization_code
            session.add(item)
            session.commit()

            resp.status = falcon.HTTP_CREATED
            resp.location = req.relative_uri + f'/{item.instance_id}'
            resp.media = {'data': custom_asdict(item)}
        finally:
            session.close()


class Item:
    """GET and DELETE an organization's IT asset instance."""

    @falcon.before(check_scope, 'read:organizations')
    def on_get(self, req, resp, organization_code, it_asset_instance_id):
        """GETs a single instance of IT asset of an organization.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        :param organization_code: The code of the organization.
        :param it_asset_instance_id: The id of the IT asset instance to retrieve.
        """
        session = Session()
        try:
            item = find_it_asset_instance(it_asset_instance_id, organization_code, session)
            if item is None:
                raise falcon.HTTPNotFound()

            resp.media = {'data': custom_asdict(item)}
        finally:
            session.close()

    @falcon.before(check_scope, 'manage:organizations')
    def on_patch(self, req, resp, organization_code, it_asset_instance_id):
        """Updates (partially) the IT asset instance requested.
        All entities that reference the IT asset instance will be affected by the update.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        :param organization_code: The code of organization.
        :param it_asset_instance_id: The id of IT asset instance to be patched.
        """
        session = Session()
        try:
            it_asset_instance = find_it_asset_instance(it_asset_instance_id, organization_code, session)
            if it_asset_instance is None:
                raise falcon.HTTPNotFound()

            errors = validate_patch(req.media, it_asset_instance, organization_code, session)
            if errors:
                raise HTTPUnprocessableEntity(errors)

            patch_item(it_asset_instance, req.media, only=['external_identifier'])
            session.commit()

            resp.status = falcon.HTTP_OK
            resp.media = {'data': custom_asdict(it_asset_instance)}
        finally:
            session.close()

    @falcon.before(check_scope, 'manage:organizations')
    def on_delete(self, req, resp, organization_code, it_asset_instance_id):
        """Removes an IT asset from an organization's IT service instance.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        :param organization_code: The code of the organization.
        :param it_asset_instance_id: The id of the IT asset instance to be removed.
        """
        session = Session()
        try:
            item = find_it_asset_instance(it_asset_instance_id, organization_code, session)
            if item is None:
                raise falcon.HTTPNotFound()

            session.delete(item)
            session.commit()
        finally:
            session.close()


def validate_post(request_media, organization_code, session):
    errors = []

    # Validate IT asset id
    # -----------------------------------------------------
    it_asset_id = request_media.get('it_asset_id')
    if it_asset_id is None:
        errors.append(build_error(Message.ERR_FIELD_CANNOT_BE_NULL, field_name='itAssetId'))
    elif not session.query(ITAsset).get(it_asset_id):
        errors.append(build_error(Message.ERR_FIELD_VALUE_INVALID, field_name='itAssetId'))

    # Validate external identifier if informed
    # There MUST NOT exist the same (IT asset id + external identifier) combination in organization
    # -----------------------------------------------------
    external_identifier = request_media.get('external_identifier')
    error = validate_str('externalIdentifier', external_identifier, max_length=constants.GENERAL_NAME_MAX_LENGTH)
    if error:
        errors.append(error)
    elif exists_it_asset(session, organization_code, it_asset_id, external_identifier):
        errors.append(build_error(Message.ERR_FIELD_VALUE_ALREADY_EXISTS, field_name='externalIdentifier'))

    return errors


def validate_patch(request_media, it_asset_instance, organization_code, session):
    errors = []

    if not request_media:
        errors.append(build_error(Message.ERR_NO_CONTENT))
        return errors

    # Validate external identifier if informed
    # There MUST NOT exist the same (IT asset id + external identifier) combination in organization except itself
    # -----------------------------------------------------
    if 'external_identifier' in request_media:
        external_identifier = request_media.get('external_identifier')
        error = validate_str('externalIdentifier', external_identifier, max_length=constants.GENERAL_NAME_MAX_LENGTH)
        if error:
            errors.append(error)
        elif exists_other_it_asset(session, organization_code, it_asset_instance, external_identifier):
            errors.append(build_error(Message.ERR_FIELD_VALUE_ALREADY_EXISTS, field_name='externalIdentifier'))

    return errors


def find_it_asset_instance(it_asset_instance_id, organization_id, session):
    query = session \
        .query(OrganizationITAsset) \
        .filter(OrganizationITAsset.instance_id == it_asset_instance_id) \
        .filter(OrganizationITAsset.organization_id == organization_id)

    return query.first()


def exists_it_asset(session, organization_code, it_asset_id, external_identifier):
    query = session\
        .query(func.count(OrganizationITAsset.instance_id))\
        .filter(OrganizationITAsset.organization_id == organization_code)\
        .filter(OrganizationITAsset.it_asset_id == it_asset_id)\
        .filter(OrganizationITAsset.external_identifier == external_identifier)

    return query.scalar()


def exists_other_it_asset(session, organization_code, it_asset_instance, external_identifier):
    query = session\
        .query(func.count(OrganizationITAsset.instance_id))\
        .filter(OrganizationITAsset.organization_id == organization_code)\
        .filter(OrganizationITAsset.it_asset_id == it_asset_instance.it_asset_id)\
        .filter(OrganizationITAsset.external_identifier == external_identifier)\
        .filter(OrganizationITAsset.instance_id != it_asset_instance.instance_id)

    return query.scalar()


def custom_asdict(dictable_model):
    exclude = ['organization_id', 'it_asset_id']
    follow = {
        'it_asset': {'only': ['id', 'name']}
    }
    return dictable_model.asdict(follow=follow, exclude=exclude)
