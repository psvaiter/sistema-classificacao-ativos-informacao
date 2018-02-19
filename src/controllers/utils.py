"""
Utility and helper methods to be used in controllers.
"""
import math
import app_constants
from errors import build_error, Message


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
    # Get (or adjust) page
    page = req.get_param_as_int('page')
    if page is None or page < 1:
        page = 1

    # Get (or adjust) records per page
    records_per_page = req.get_param_as_int('recordsPerPage')
    if records_per_page is None or records_per_page < 1:
        records_per_page = app_constants.DEFAULT_RECORDS_PER_PAGE
    records_per_page = min(records_per_page, app_constants.MAX_RECORDS_PER_PAGE)

    # Go fetch data
    records, page, total_records = query_page(query, page, records_per_page)
    data = [record.asdict() for record in records]
    paging = build_paging_info(page, records_per_page, total_records)

    return data, paging


def query_page(query, page, records_per_page):
    total_records = query.count()
    total_pages = math.ceil(total_records / records_per_page) or 1

    # Adjust page and offset after fetching the actual number of records
    # that would be returned from database. This ensures safe limits
    # and return the last page when requested page is too high.
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
        'total_pages': math.ceil(total_records / records_per_page) or 1,
        'total_records': total_records
    }


def validate_str(field_name, field_value, is_mandatory=False, max_length=None, exists_strategy=None):
    """Validates a string with general predefined rules.

    :param field_name: The field name to put in error object.
    :param field_value: The field value to be validated.
    :param is_mandatory: Indicates that the field is mandatory. That means that
        an error is returned if value is None, empty or whitespaces only.
        Default is false.
    :param max_length: Maximum length allowed. An error is returned if len(field_value)
        is above this value. When None, this validation will be skipped.
        Default is None.
    :param exists_strategy: A function that returns something or True when value
        already exists. If the function returns None or False, the value is
        considered new and validation will pass. If function is None, this
        validation will be skipped.
        Default is None.
    :return: A dict containing an error code, a message and the field name.
    """
    # Field was not informed...
    if field_value is None:
        if is_mandatory:
            return build_error(Message.ERR_FIELD_CANNOT_BE_NULL, field_name=field_name)

        # OK, it's not mandatory.
        return None

    # Must be of type 'string'
    if not isinstance(field_value, str):
        return build_error(Message.ERR_FIELD_VALUE_MUST_BE_STRING, field_name=field_name)

    # Remove leading and trailing whitespaces from value before continuing
    # It's better to trim here in order to validate the length that will be
    # actually saved and to compare with existing values appropriately.
    # Also a value with only whitespaces will become an empty string.
    field_value = field_value.strip()

    # Cannot be empty (general safe rule whether it's mandatory or not)
    if not field_value:
        return build_error(Message.ERR_FIELD_CANNOT_BE_EMPTY, field_name=field_name)

    # Length must be valid
    if len(field_value) > max_length:
        return build_error(Message.ERR_FIELD_MAX_LENGTH, field_name=field_name)

    # Must be unique
    if exists_strategy and exists_strategy():
        return build_error(Message.ERR_FIELD_VALUE_ALREADY_EXISTS, field_name=field_name)
