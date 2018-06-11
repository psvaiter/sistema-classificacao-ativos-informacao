import falcon
from .extensions import HTTPUnprocessableEntity
from .utils import get_collection_page, patch_item, validate_str
from errors import Message, build_error
from models import Session, OrganizationITAsset, Organization, ITAsset
import app_constants as constants


class Collection:
    """GET and POST IT assets of an organization."""

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
                .query(OrganizationITAsset) \
                .filter(OrganizationITAsset.organization_id == organization_code)\
                .order_by(OrganizationITAsset.created_on)

            data, paging = get_collection_page(req, query, custom_asdict)
            resp.media = {
                'data': data,
                'paging': paging
            }
        finally:
            session.close()

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
            resp.location = req.relative_uri
            resp.media = {'data': custom_asdict(item)}
        finally:
            session.close()


class Item:
    """GET and DELETE an organization's IT asset instance."""

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

            errors = validate_patch(req.media, organization_code, session)
            if errors:
                raise HTTPUnprocessableEntity(errors)

            patch_item(it_asset_instance, req.media, only=['external_identifier'])
            session.commit()

            resp.status = falcon.HTTP_OK
            resp.media = {'data': custom_asdict(it_asset_instance)}
        finally:
            session.close()

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

    # Validate IT asset instance id
    # -----------------------------------------------------
    it_asset_id = request_media.get('it_asset_id')
    if it_asset_id is None:
        errors.append(build_error(Message.ERR_FIELD_CANNOT_BE_NULL, field_name='itAssetId'))
    elif not session.query(ITAsset).get(it_asset_id):
        errors.append(build_error(Message.ERR_FIELD_VALUE_INVALID, field_name='itAssetId'))

    # Validate external identifier if informed
    # -----------------------------------------------------
    external_identifier = request_media.get('external_identifier')
    error = validate_str('externalIdentifier', external_identifier, max_length=constants.GENERAL_NAME_MAX_LENGTH)
    if error:
        errors.append(error)

    # TODO: validate if an IT asset with the same external identifier already exists in organization

    return errors


def validate_patch(request_media, organization_code, session):
    errors = []

    if not request_media:
        errors.append(build_error(Message.ERR_NO_CONTENT))
        return errors

    # Validate external identifier if informed
    # -----------------------------------------------------
    if 'external_identifier' in request_media:
        external_identifier = request_media.get('external_identifier')
        error = validate_str('externalIdentifier', external_identifier, max_length=constants.GENERAL_NAME_MAX_LENGTH)
        if error:
            errors.append(error)

    # TODO: validate if an IT asset with the same external identifier already exists in organization

    return errors


def find_it_asset_instance(it_asset_instance_id, organization_id, session):
    query = session \
        .query(OrganizationITAsset) \
        .filter(OrganizationITAsset.instance_id == it_asset_instance_id) \
        .filter(OrganizationITAsset.organization_id == organization_id)

    return query.first()


def custom_asdict(dictable_model):
    exclude = ['organization_id', 'it_asset_id']
    include = {
        'it_asset': {'only': ['id', 'name']}
    }
    return dictable_model.asdict(follow=include, exclude=exclude)
