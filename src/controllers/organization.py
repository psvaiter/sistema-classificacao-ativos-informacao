import falcon

import app_constants as constants
from .extensions import HTTPUnprocessableEntity
from .utils import get_collection_page
from errors import Message
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
            organization = Organization.fromdict(req.media)
            session.add(organization)
            session.commit()
            response_data = organization.asdict()
        finally:
            session.close()

        resp.status = falcon.HTTP_CREATED
        resp.media = {'data': response_data}


def validate_organization_patch(request, session):
    return []


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


def validate_organization(request, session):
    errors = []

    # Tax ID is mandatory and must be unique. Validate length.
    tax_id = request.get('taxId')
    if tax_id is None:
        errors.append(crerror(Message.ERR_TAX_ID_MANDATORY))
    elif session.query(Organization.tax_id)\
            .filter_by(tax_id=request.get('taxId'))\
            .exists() is not None:
        errors.append(crerror(Message.ERR_TAX_ID_ALREADY_EXISTS))
    elif len(tax_id) > constants.TAX_ID_MAX_LENGTH:
        errors.append(crerror(Message.ERR_TAX_ID_MAX_LENGTH))

    # Legal name is mandatory. Validate length.
    legal_name = request.get('legalName')
    if legal_name is None:
        errors.append(crerror(Message.ERR_LEGAL_NAME_MANDATORY))
    elif len(legal_name) > constants.GENERAL_NAME_MAX_LENGTH:
        errors.append(crerror(Message.ERR_LEGAL_NAME_MAX_LENGTH))

    # Trade name is optional. Validate length when informed.
    trade_name = request.get('tradeName')
    if len(trade_name) > constants.GENERAL_NAME_MAX_LENGTH:
        errors.append(crerror(Message.ERR_TRADE_NAME_MAX_LENGTH))

    return errors


def get_message(message_enum, lang):
    return message_enum.value


def crerror(message_enum, lang="pt-BR", field_name=None):
    return dict(
        code=message_enum.name,
        message=get_message(message_enum, lang)
    )


def map_from_request(request):
    return Organization(
        tax_id=request['taxId'],
        legal_name=request['legalName'],
        trade_name=request['tradeName']
    )


def map_to_response(organization):
    return dict(
        organizationId=organization.organization_id,
        legalName=organization.legal_name,
        tradeName=organization.trade_name,
        taxId=organization.tax_id,
        createdOn=organization.created_on.isoformat(),
        lastModifiedOn=organization.last_modified_on.isoformat()
    )
