"""
Utility and helper methods to be used in controllers.
"""
import math
import app_constants


def get_collection_page(req, query):
    """
    Common implementation used by controllers to fetch collection of an entity.
    The result is paged. Paging params can be informed in URL query string.
        'recordsPerPage': Number of records that each page will contain at most.
            Max value allowed is MAX_RECORDS_PER_PAGE.
            Default is DEFAULT_RECORDS_PER_PAGE.
        'page': desired page number.
            Default is 1.

    :param req: The request object. See Falcon Request documentation.
        Query string arguments are extracted from this object.
    :param query: Session query from SQL Alchemy to fetch records.
    :return: A dict with 'data' and 'paging' keys.
    """
    page = req.get_param_as_int('page') or 1
    records_per_page = req.get_param_as_int('recordsPerPage') or app_constants.DEFAULT_RECORDS_PER_PAGE
    records_per_page = min(records_per_page, app_constants.MAX_RECORDS_PER_PAGE)

    records, page, total_records = query_page(query, page, records_per_page)
    data = [record.asdict() for record in records]
    paging = build_paging_info(page, records_per_page, total_records)

    return data, paging


def query_page(query, page, records_per_page):
    total_records = query.count()
    total_pages = math.ceil(total_records / records_per_page)

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


def build_paging_info(page, records_per_page, total_records):
    return {
        'current_page': page,
        'records_per_page': records_per_page,
        'total_pages': math.ceil(total_records / records_per_page),
        'total_records': total_records
    }
