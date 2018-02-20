import falcon
from datetime import datetime

import app_constants as constants
from .extensions import HTTPUnprocessableEntity
from .utils import get_collection_page, validate_str
from errors import Message, build_error
from models import Session, ITAssetCategory


class Collection:
    """GET and POST IT asset categories in catalog."""

    def on_get(self, req, resp):
        """GETs a paged collection of IT asset categories available.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        """
        session = Session()
        try:
            query = session.query(ITAssetCategory).order_by(ITAssetCategory.created_on)

            data, paging = get_collection_page(req, query)
            resp.media = {
                'data': data,
                'paging': paging
            }
        finally:
            session.close()

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
            item = ITAssetCategory().fromdict(req.media, only=['category_id', 'name'])

            session.add(item)
            session.commit()
            resp.status = falcon.HTTP_CREATED
            resp.media = {'data': item.asdict()}
        finally:
            session.close()


class Item:
    """GET and PATCH an IT asset category in catalog."""

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

    def on_patch(self, req, resp, it_asset_category_id):
        """Updates (partially) the IT asset category requested.
        All entities that reference the IT asset category will be affected by the update.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        :param it_asset_category_id: The id of IT asset category to be patched.
        """
        session = Session()
        try:
            it_asset = session.query(ITAssetCategory).get(it_asset_category_id)
            if it_asset is None:
                raise falcon.HTTPNotFound()

            errors = validate_patch(req.media, session)
            if errors:
                raise HTTPUnprocessableEntity(errors)

            # Apply fields informed in request, compare before and after
            # and save patch only if record has changed.
            old_it_asset = it_asset.asdict()
            it_asset.fromdict(req.media, only=['name'])
            new_it_asset = it_asset.asdict()
            if new_it_asset != old_it_asset:
                it_asset.last_modified_on = datetime.utcnow()
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

    # Asset category id is mandatory and must be available
    # -----------------------------------------------------
    category_id = request_media.get('category_id')
    if category_id is None:
        errors.append(build_error(Message.ERR_IT_ASSET_CATEGORY_ID_CANNOT_BE_NULL, field_name='category_id'))
    elif session.query(ITAssetCategory).get(category_id) is not None:
        errors.append(build_error(Message.ERR_IT_ASSET_CATEGORY_ID_ALREADY_EXISTS, field_name='category_id'))

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
