import falcon

from knoweak.api import constants as constants
from knoweak.api.errors import Message, build_error
from knoweak.api.extensions import HTTPUnprocessableEntity
from knoweak.api.middlewares.auth import check_scope
from knoweak.api.utils import get_collection_page, validate_str, patch_item
from knoweak.db import Session
from knoweak.db.models.organization import Organization


class Collection:
    """GET and POST organizations."""

    @falcon.before(check_scope, 'read:organizations')
    def on_get(self, req, resp):
        """GETs a paged collection of organizations.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        """
        session = Session()
        try:
            query = session.query(Organization).order_by(Organization.legal_name, Organization.created_on)

            data, paging = get_collection_page(req, query)
            resp.media = {
                'data': data,
                'paging': paging
            }
        finally:
            session.close()

    @falcon.before(check_scope, 'create:organizations')
    def on_post(self, req, resp):
        """Creates a new organization.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        """
        session = Session()
        try:
            errors = validate_post(req.media, session)
            if errors:
                raise HTTPUnprocessableEntity(errors)

            # Copy fields from request to an Organization object
            accepted_fields = ['tax_id', 'legal_name', 'trade_name']
            item = Organization().fromdict(req.media, only=accepted_fields)

            session.add(item)
            session.commit()
            resp.status = falcon.HTTP_CREATED
            resp.location = req.relative_uri + f'/{item.id}'
            resp.media = {'data': item.asdict()}
        finally:
            session.close()


class Item:
    """GET and PATCH an organization."""

    @falcon.before(check_scope, 'read:organizations')
    def on_get(self, req, resp, organization_code):
        """GETs a single organization by its code.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        :param organization_code: The code of organization to retrieve.
        """
        session = Session()
        try:
            item = session.query(Organization).get(organization_code)
            if item is None:
                raise falcon.HTTPNotFound()

            resp.media = {'data': item.asdict()}
        finally:
            session.close()

    @falcon.before(check_scope, 'update:organizations')
    def on_patch(self, req, resp, organization_code):
        """Updates (partially) the organization.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        :param organization_code: The code of organization to be patched.
        """
        session = Session()
        try:
            organization = session.query(Organization).get(organization_code)
            if organization is None:
                raise falcon.HTTPNotFound()

            errors = validate_patch(req.media, session)
            if errors:
                raise HTTPUnprocessableEntity(errors)

            patch_item(organization, req.media, only=['tax_id', 'legal_name', 'trade_name'])
            session.commit()

            resp.status = falcon.HTTP_OK
            resp.media = {'data': organization.asdict()}
        finally:
            session.close()


def validate_post(request_media, session):
    errors = []

    # Validate Tax ID
    # -----------------------------------------------------
    tax_id = request_media.get('tax_id')
    error = validate_str('taxId', tax_id,
                         is_mandatory=True,
                         max_length=constants.TAX_ID_MAX_LENGTH,
                         exists_strategy=exists_tax_id(tax_id, session))
    if error:
        errors.append(error)

    # Validate legal name
    # -----------------------------------------------------
    legal_name = request_media.get('legal_name')
    error = validate_str('legalName', legal_name,
                         is_mandatory=True,
                         min_length=constants.GENERAL_NAME_MIN_LENGTH,
                         max_length=constants.GENERAL_NAME_MAX_LENGTH)
    if error:
        errors.append(error)

    # Validate trade name
    # -----------------------------------------------------
    trade_name = request_media.get('trade_name')
    error = validate_str('tradeName', trade_name,
                         min_length=constants.GENERAL_NAME_MIN_LENGTH,
                         max_length=constants.GENERAL_NAME_MAX_LENGTH)
    if error:
        errors.append(error)

    return errors


def validate_patch(request_media, session):
    errors = []

    if not request_media:
        errors.append(build_error(Message.ERR_NO_CONTENT))
        return errors

    # Validate Tax ID if informed
    # -----------------------------------------------------
    if 'tax_id' in request_media:
        tax_id = request_media.get('tax_id')
        error = validate_str('taxId', tax_id,
                             is_mandatory=True,
                             max_length=constants.TAX_ID_MAX_LENGTH,
                             exists_strategy=exists_tax_id(tax_id, session))
        if error:
            errors.append(error)

    # Validate legal name if informed
    # -----------------------------------------------------
    if 'legal_name' in request_media:
        legal_name = request_media.get('legal_name')
        error = validate_str('legalName', legal_name,
                             is_mandatory=True,
                             min_length=constants.GENERAL_NAME_MIN_LENGTH,
                             max_length=constants.GENERAL_NAME_MAX_LENGTH)
        if error:
            errors.append(error)

    # Validate trade name if informed
    # -----------------------------------------------------
    if 'trade_name' in request_media:
        trade_name = request_media.get('trade_name')
        error = validate_str('tradeName', trade_name,
                             min_length=constants.GENERAL_NAME_MIN_LENGTH,
                             max_length=constants.GENERAL_NAME_MAX_LENGTH)
        if error:
            errors.append(error)

    return errors


def exists_tax_id(tax_id, session):
    def exists():
        return session.query(Organization.tax_id) \
            .filter(Organization.tax_id == tax_id) \
            .first()
    return exists
