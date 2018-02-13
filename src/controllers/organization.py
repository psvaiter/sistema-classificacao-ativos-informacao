import falcon
from datetime import datetime

import app_constants as constants
from .extensions import HTTPUnprocessableEntity
from .utils import get_collection_page
from errors import Message, build_error
from models import Session, Organization


class Collection:

    def on_get(self, req, resp):
        """
        GETs a paged collection of organizations.

        Paging parameters can be informed in querystring:
            'recordsPerPage': Number of records that each page will contain. Default is 10.
            'page': desired page number. Default is 1.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        :return:
        """
        session = Session()
        query = session.query(Organization).order_by(Organization.created_on)

        data, paging = get_collection_page(req, query)
        resp.media = {
            'data': data,
            'paging': paging
        }

    def on_post(self, req, resp):
        """
        Creates a new organization.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        :return:
        """
        session = Session()
        try:
            errors = validate_organization(req.media, session)
            if errors:
                raise HTTPUnprocessableEntity(errors)
            organization = Organization().fromdict(req.media)
            session.add(organization)
            session.commit()
            response_data = organization.asdict()
        finally:
            session.close()

        resp.status = falcon.HTTP_CREATED
        resp.media = {'data': response_data}


class Item:

    def on_get(self, req, resp, organization_code):
        """
        GETs a single organization by its code.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        :param organization_code: The code of organization to retrieve.
        :return:
        """
        session = Session()
        organization = session.query(Organization).get(organization_code)
        if organization is None:
            raise falcon.HTTPNotFound()

        resp.media = {'data': organization.asdict()}

    def on_patch(self, req, resp, organization_code):
        """
        Updates (partially) the organization.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        :param organization_code: The code of organization to be patched.
        :return:
        """
        session = Session()
        try:
            organization = session.query(Organization).get(organization_code)
            if organization is None:
                raise falcon.HTTPNotFound()

            errors = validate_organization_patch(req.media, session)
            if errors:
                raise HTTPUnprocessableEntity(errors)

            old_organization = organization.asdict()
            organization.fromdict(req.media, only=['tax_id', 'legal_name', 'trade_name'])
            new_organization = organization.asdict()
            if new_organization != old_organization:
                organization.last_modified_on = datetime.utcnow()

            session.commit()

            resp.status = falcon.HTTP_OK
            resp.media = {'data': organization.asdict()}
        finally:
            session.close()


def validate_organization(request_media, session):
    errors = []

    # Tax ID is mandatory and must be unique. Validate length.
    tax_id = request_media.get('tax_id')
    if tax_id is None:
        errors.append(build_error(Message.ERR_TAX_ID_MANDATORY))
    elif len(tax_id) > constants.TAX_ID_MAX_LENGTH:
        errors.append(build_error(Message.ERR_TAX_ID_MAX_LENGTH))
    elif session.query(Organization.tax_id)\
            .filter_by(tax_id=tax_id)\
            .first():
        errors.append(build_error(Message.ERR_TAX_ID_ALREADY_EXISTS))

    # Legal name is mandatory. Validate length.
    legal_name = request_media.get('legal_name')
    if legal_name is None:
        errors.append(build_error(Message.ERR_LEGAL_NAME_MANDATORY))
    elif len(legal_name) > constants.GENERAL_NAME_MAX_LENGTH:
        errors.append(build_error(Message.ERR_LEGAL_NAME_MAX_LENGTH))

    # Trade name is optional. Validate length when informed.
    trade_name = request_media.get('trade_name')
    if trade_name and len(trade_name) > constants.GENERAL_NAME_MAX_LENGTH:
        errors.append(build_error(Message.ERR_TRADE_NAME_MAX_LENGTH))

    return errors


def validate_organization_patch(request_media, session):
    errors = []

    if not request_media:
        errors.append(build_error(Message.ERR_NO_CONTENT))
        return errors

    # Tax ID can be informed and must be unique. Validate length.
    tax_id = request_media.get('tax_id')
    if tax_id:
        if len(tax_id) > constants.TAX_ID_MAX_LENGTH:
            errors.append(build_error(Message.ERR_TAX_ID_MAX_LENGTH))
        elif session.query(Organization.tax_id) \
                .filter_by(tax_id=tax_id) \
                .first():
            errors.append(build_error(Message.ERR_TAX_ID_ALREADY_EXISTS))

    # Legal name is optional. Validate length when informed.
    legal_name = request_media.get('legal_name')
    if legal_name and len(legal_name) > constants.GENERAL_NAME_MAX_LENGTH:
        errors.append(build_error(Message.ERR_LEGAL_NAME_MAX_LENGTH))

    # Trade name is optional. Validate length when informed.
    trade_name = request_media.get('trade_name')
    if trade_name and len(trade_name) > constants.GENERAL_NAME_MAX_LENGTH:
        errors.append(build_error(Message.ERR_TRADE_NAME_MAX_LENGTH))

    return errors
