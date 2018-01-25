import json
from models import Session, Organization
import app_constants as constants


class Collection:

    def on_get(self, req, resp):

        page = req.get_param_as_int('page') or 1
        records_per_page = req.get_param_as_int('recordsPerPage') or constants.DEFAULT_RECORDS_PER_PAGE
        records_per_page = min(records_per_page, constants.MAX_RECORDS_PER_PAGE)

        session = Session()
        query = session.query(Organization).order_by(Organization.created_on)
        organizations, page, total_records = query_page(query, page, records_per_page)

        data = [map_to_response(organization) for organization in organizations]
        paging = build_paging_info(page, records_per_page, total_records)
        body = dict(data=data, paging=paging)

        resp.body = json.dumps(body)


def query_page(query, page, records_per_page):

    total_records = query.count()
    total_pages = int(total_records / records_per_page) + 1

    # Adjust page and offset after fetching the actual number of records
    # that would be returned from database. This ensures safe limits.
    if page <= 0:
        page = 1
    page = min(page, total_pages)
    offset = (page - 1) * records_per_page

    result = query \
        .limit(records_per_page) \
        .offset(offset) \
        .all()

    return result, page, total_records


def map_to_response(organization):
    return dict(
        organizationId=organization.organization_id,
        legalName=organization.legal_name,
        tradeName=organization.trade_name,
        taxId=organization.tax_id,
        createdOn=organization.created_on.isoformat(),
        lastModifiedOn=organization.last_modified_on.isoformat()
    )


def build_paged_response(response, page, records_per_page, total_records):
    paged_response = response
    paged_response.paging = build_paging_info(page, records_per_page, total_records)

    return paged_response


def build_paging_info(page, records_per_page, total_records):
    paging = dict(currentPage=page,
                  recordsPerPage=records_per_page,
                  totalPages=int(total_records / records_per_page) + 1,
                  totalRecords=total_records)
    return paging


class Item:
    pass
