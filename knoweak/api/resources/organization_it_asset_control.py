import falcon

from knoweak.api import constants as constants
from knoweak.api.errors import build_error, Message
from knoweak.api.middlewares.auth import check_scope
from knoweak.api.utils import validate_str, get_collection_page
from knoweak.api.extensions import HTTPUnprocessableEntity
from knoweak.db import Session
from knoweak.db.models.catalog import MitigationControl
from knoweak.db.models.organization import OrganizationItAssetControl, OrganizationITAsset


class Collection:
    """GET and POST mitigation controls for organization IT assets."""

    @falcon.before(check_scope, 'manage:organizations')
    def on_get(self, req, resp, organization_code, it_asset_instance_id):
        """List mitigation controls for an organization IT asset.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        :param organization_code: The code of the organization.
        :param it_asset_instance_id: The id of the IT asset instance.
        """
        session = Session()
        try:
            organization_it_asset = find_organization_it_asset(it_asset_instance_id, organization_code, session)
            if organization_it_asset is None:
                raise falcon.HTTPNotFound()

            # Build query to fetch items
            query = session \
                .query(OrganizationItAssetControl) \
                .join(OrganizationITAsset) \
                .join(MitigationControl) \
                .filter(OrganizationITAsset.organization_id == organization_code) \
                .filter(OrganizationITAsset.instance_id == it_asset_instance_id) \
                .order_by(MitigationControl.name)

            data, paging = get_collection_page(req, query, custom_asdict)
            resp.media = {
                'data': data,
                'paging': paging
            }
        finally:
            session.close()

    @falcon.before(check_scope, 'manage:organizations')
    def on_post(self, req, resp, organization_code, it_asset_instance_id):
        """Adds a control to an IT asset in order to decrease vulnerability against a security threat.
        However, the security threat against which the control is effective is not relevant here.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        :param organization_code: The code of the organization.
        :param it_asset_instance_id: The id of the IT asset instance.
        """
        session = Session()
        try:
            organization_it_asset = find_organization_it_asset(it_asset_instance_id, organization_code, session)
            if organization_it_asset is None:
                raise falcon.HTTPNotFound()

            errors = validate_post(req.media, it_asset_instance_id, organization_code, session)
            if errors:
                raise HTTPUnprocessableEntity(errors)

            accepted_fields = ['mitigation_control_id', 'description']
            item = OrganizationItAssetControl().fromdict(req.media, only=accepted_fields)
            item.organization_it_asset_id = it_asset_instance_id
            session.add(item)
            session.commit()

            resp.status = falcon.HTTP_CREATED
            resp.location = req.relative_uri + f'/{item.id}'
            resp.media = {'data': custom_asdict(item)}
        finally:
            session.close()


class Item:
    """DELETE a mitigation control from organization IT asset."""

    @falcon.before(check_scope, 'manage:organizations')
    def on_delete(self, req, resp, organization_code, it_asset_instance_id, control_id):
        """Removes a control from an IT asset.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        :param organization_code: The code of the organization.
        :param it_asset_instance_id: The id of the IT asset instance.
        :param control_id: The id of the control to be removed.
        """
        session = Session()
        try:
            item = find_it_asset_control(control_id, it_asset_instance_id, organization_code, session)
            if item is None:
                raise falcon.HTTPNotFound()

            session.delete(item)
            session.commit()
        finally:
            session.close()


def validate_post(request_media, it_asset_instance_id, organization_code, session):
    errors = []

    # Validate mitigation control id
    # -----------------------------------------------------
    mitigation_control_id = request_media.get('mitigation_control_id')
    if mitigation_control_id is None:
        errors.append(build_error(Message.ERR_FIELD_CANNOT_BE_NULL, field_name='mitigationControlId'))
    elif not session.query(MitigationControl).get(mitigation_control_id):
        errors.append(build_error(Message.ERR_FIELD_VALUE_INVALID, field_name='mitigationControlId'))
    elif find_it_asset_control(mitigation_control_id, it_asset_instance_id, organization_code, session):
        errors.append(build_error(Message.ERR_FIELD_VALUE_ALREADY_EXISTS, field_name='mitigationControlId'))

    # Validate description if informed
    # -----------------------------------------------------
    description = request_media.get('description')
    error = validate_str('description', description, max_length=constants.GENERAL_DESCRIPTION_MAX_LENGTH)
    if error:
        errors.append(error)

    return errors


def find_it_asset_control(mitigation_control_id, it_asset_instance_id, organization_code, session):
    query = session \
        .query(OrganizationItAssetControl) \
        .join(OrganizationITAsset) \
        .filter(OrganizationItAssetControl.mitigation_control_id == mitigation_control_id) \
        .filter(OrganizationITAsset.instance_id == it_asset_instance_id) \
        .filter(OrganizationITAsset.organization_id == organization_code)

    return query.first()


def find_organization_it_asset(it_asset_instance_id, organization_code, session):
    query = session \
        .query(OrganizationITAsset) \
        .filter(OrganizationITAsset.instance_id == it_asset_instance_id) \
        .filter(OrganizationITAsset.organization_id == organization_code)

    return query.first()


def custom_asdict(dictable_model):
    exclude = [
        'organization_it_asset_id',
        'mitigation_control_id'
    ]
    follow = {
        'mitigation_control': {'only': ['id', 'name']}
    }
    return dictable_model.asdict(follow=follow, exclude=exclude)
