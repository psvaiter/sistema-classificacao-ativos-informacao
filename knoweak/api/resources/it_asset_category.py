import falcon

from knoweak.api import constants as constants
from knoweak.api.errors import Message, build_error
from knoweak.api.extensions import HTTPUnprocessableEntity
from knoweak.api.middlewares.auth import check_scope
from knoweak.api.utils import get_collection_page, validate_str, patch_item, validate_number
from knoweak.db import Session
from knoweak.db.models.catalog import ITAssetCategory


class Collection:
    """GET and POST IT asset categories in catalog."""

    @falcon.before(check_scope, 'read:catalog')
    def on_get(self, req, resp):
        """GETs a paged collection of IT asset categories available.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        """
        session = Session()
        try:
            query = session.query(ITAssetCategory).order_by(ITAssetCategory.name)

            data, paging = get_collection_page(req, query)
            resp.media = {
                'data': data,
                'paging': paging
            }
        finally:
            session.close()

    @falcon.before(check_scope, 'create:catalog')
    def on_post(self, req, resp):
        """Creates a new IT asset category in catalog.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        """
        session = Session()
        try:
            errors = validate_post(req.media, session)
            if errors:
                raise HTTPUnprocessableEntity(errors)

            # Copy fields from request to an ITAssetCategory object
            item = ITAssetCategory().fromdict(req.media, only=['id', 'name'])

            session.add(item)
            session.commit()
            resp.status = falcon.HTTP_CREATED
            resp.location = req.relative_uri + f'/{item.id}'
            resp.media = {'data': item.asdict()}
        finally:
            session.close()


class Item:
    """GET and PATCH an IT asset category in catalog."""

    @falcon.before(check_scope, 'read:catalog')
    def on_get(self, req, resp, it_asset_category_id):
        """GETs a single IT asset by id.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        :param it_asset_category_id: The id of IT asset category to retrieve.
        """
        session = Session()
        try:
            item = session.query(ITAssetCategory).get(it_asset_category_id)
            if item is None:
                raise falcon.HTTPNotFound()

            resp.media = {'data': item.asdict()}
        finally:
            session.close()

    @falcon.before(check_scope, 'update:catalog')
    def on_patch(self, req, resp, it_asset_category_id):
        """Updates (partially) the IT asset category requested.
        All entities that reference the IT asset category will be affected by the update.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        :param it_asset_category_id: The id of IT asset category to be patched.
        """
        session = Session()
        try:
            it_asset_category = session.query(ITAssetCategory).get(it_asset_category_id)
            if it_asset_category is None:
                raise falcon.HTTPNotFound()

            errors = validate_patch(req.media, session)
            if errors:
                raise HTTPUnprocessableEntity(errors)

            patch_item(it_asset_category, req.media, only=['name'])
            session.commit()

            resp.status = falcon.HTTP_OK
            resp.media = {'data': it_asset_category.asdict()}
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

    # Category id is mandatory, must be valid and must be available
    # -----------------------------------------------------
    category_id = request_media.get('id')
    error = validate_number('id', category_id,
                            is_mandatory=True,
                            min_value=1,
                            exists_strategy=lambda: session.query(ITAssetCategory).get(category_id))
    if errors:
        errors.append(error)

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

    return errors


def exists_name(name, session):
    def exists():
        return session.query(ITAssetCategory.name) \
            .filter(ITAssetCategory.name == name) \
            .first()
    return exists
