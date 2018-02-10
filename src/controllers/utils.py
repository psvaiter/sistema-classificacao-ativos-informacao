"""
Utility and helper methods to be used in controllers.
"""


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
