import json
import falcon
from models import Session, Organization
from . import utils
import app_constants as constants


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

        page = req.get_param_as_int('page') or 1
        records_per_page = req.get_param_as_int('recordsPerPage') or constants.DEFAULT_RECORDS_PER_PAGE
        records_per_page = min(records_per_page, constants.MAX_RECORDS_PER_PAGE)

        session = Session()
        query = session.query(Organization).order_by(Organization.created_on)
        organizations, page, total_records = utils.query_page(query, page, records_per_page)

        data = [map_to_response(organization) for organization in organizations]
        paging = utils.build_paging_info(page, records_per_page, total_records)
        body = dict(data=data, paging=paging)

        resp.body = json.dumps(body)

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
            if errors is not None:
                resp.status = falcon.HTTPUnprocessableEntity
                resp.media = errors
                return

            organization = map_from_request(req.media)
            session.add(organization)
            session.commit()
            response_data = map_to_response(organization)
        finally:
            session.close()

        resp.status = falcon.HTTP_CREATED
        resp.media = dict(data=response_data)


class Item:

    def on_get(self, req, resp, organization_code):
        """
        GETs a single organization by its code.

        :param req: See Falcon Request documentation.
        :param resp: See Falcon Response documentation.
        :param organization_code: A organization code.
        :return:
        """

        session = Session()
        organization = session.query(Organization).get(organization_code)
        if organization is None:
            raise falcon.HTTPNotFound()

        data = map_to_response(organization)
        body = dict(data=data)

        resp.body = json.dumps(body)


def validate_organization(organization_request, session):
    pass


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
