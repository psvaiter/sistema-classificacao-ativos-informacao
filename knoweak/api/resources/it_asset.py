import falcon

from knoweak.api import constants as constants
from knoweak.api.errors import Message, build_error
from knoweak.api.extensions import HTTPUnprocessableEntity
from knoweak.api.middlewares.auth import check_scope
from knoweak.api.utils import get_collection_page, validate_str, patch_item
from knoweak.db import Session
from knoweak.db.models.catalog import ITAsset, ITAssetCategory


class Collection:
    """GET and POST IT assets in catalog."""

    @falcon.before(check_scope, 'read:catalog')
    def on_get(self, req, resp):
        """GETs a paged collection of IT assets available.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        """
        session = Session()
        try:
            query = session.query(ITAsset).order_by(ITAsset.name)

            data, paging = get_collection_page(req, query, custom_asdict)
            resp.media = {
                'data': data,
                'paging': paging
            }
        finally:
            session.close()

    @falcon.before(check_scope, 'create:catalog')
    def on_post(self, req, resp):
        """Creates a new IT asset in catalog.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        """
        session = Session()
        try:
            errors = validate_post(req.media, session)
            if errors:
                raise HTTPUnprocessableEntity(errors)

            # Copy fields from request to an ITAsset object
            item = ITAsset().fromdict(req.media, only=['name', 'description', 'category_id'])

            session.add(item)
            session.commit()
            resp.status = falcon.HTTP_CREATED
            resp.location = req.relative_uri + f'/{item.id}'
            resp.media = {'data': item.asdict()}
        finally:
            session.close()


class Item:
    """GET and PATCH an IT asset in catalog."""

    @falcon.before(check_scope, 'read:catalog')
    def on_get(self, req, resp, it_asset_id):
        """GETs a single IT asset by id.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        :param it_asset_id: The id of IT asset to retrieve.
        """
        session = Session()
        try:
            item = session.query(ITAsset).get(it_asset_id)
            if item is None:
                raise falcon.HTTPNotFound()

            resp.media = {'data': item.asdict()}
        finally:
            session.close()

    @falcon.before(check_scope, 'update:catalog')
    def on_patch(self, req, resp, it_asset_id):
        """Updates (partially) the IT asset requested.
        All entities that reference the IT asset will be affected by the update.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        :param it_asset_id: The id of IT asset to be patched.
        """
        session = Session()
        try:
            it_asset = session.query(ITAsset).get(it_asset_id)
            if it_asset is None:
                raise falcon.HTTPNotFound()

            errors = validate_patch(req.media, session)
            if errors:
                raise HTTPUnprocessableEntity(errors)

            patch_item(it_asset, req.media, only=['name', 'description', 'category_id'])
            session.commit()

            resp.status = falcon.HTTP_OK
            resp.media = {'data': it_asset.asdict()}
        finally:
            session.close()


def validate_post(request_media, session):
    errors = []

    # Validate name
    # -----------------------------------------------------
    name = request_media.get('name')
    error = validate_str('name', name,
                         is_mandatory=True,
                         max_length=constants.GENERAL_NAME_MAX_LENGTH,
                         exists_strategy=exists_name(name, session))
    if error:
        errors.append(error)

    # Validate description
    # -----------------------------------------------------
    description = request_media.get('description')
    error = validate_str('description', description, max_length=constants.GENERAL_DESCRIPTION_MAX_LENGTH)
    if error:
        errors.append(error)

    # Asset category id is mandatory and must be valid
    # -----------------------------------------------------
    category_id = request_media.get('category_id')
    if category_id is None:
        errors.append(build_error(Message.ERR_FIELD_CANNOT_BE_NULL, field_name='categoryId'))
    elif not session.query(ITAssetCategory).get(category_id):
        errors.append(build_error(Message.ERR_FIELD_VALUE_INVALID, field_name='categoryId'))

    return errors


def validate_patch(request_media, session):
    errors = []

    if not request_media:
        errors.append(build_error(Message.ERR_NO_CONTENT))
        return errors

    # Validate name if informed
    # -----------------------------------------------------
    if 'name' in request_media:
        name = request_media.get('name')
        error = validate_str('name', name,
                             is_mandatory=True,
                             max_length=constants.GENERAL_NAME_MAX_LENGTH,
                             exists_strategy=exists_name(name, session))
        if error:
            errors.append(error)

    # Validate description if informed
    # -----------------------------------------------------
    if 'description' in request_media:
        description = request_media.get('description')
        error = validate_str('description', description, max_length=constants.GENERAL_DESCRIPTION_MAX_LENGTH)
        if error:
            errors.append(error)

    # Validate asset category id if informed
    # -----------------------------------------------------
    if 'category_id' in request_media:
        category_id = request_media.get('category_id')

        # Cannot be null if informed and must be valid
        if category_id is None:
            errors.append(build_error(Message.ERR_FIELD_CANNOT_BE_NULL, field_name='categoryId'))
        elif not session.query(ITAssetCategory).get(category_id):
            errors.append(build_error(Message.ERR_FIELD_VALUE_INVALID, field_name='categoryId'))

    return errors


def exists_name(name, session):
    def exists():
        return session.query(ITAsset.name) \
            .filter(ITAsset.name == name) \
            .first()
    return exists


def custom_asdict(dictable_model):
    follow = {'category': {'only': ['id', 'name']}}
    return dictable_model.asdict(follow=follow, exclude=['category_id'])
