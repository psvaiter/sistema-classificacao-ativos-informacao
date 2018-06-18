"""
Utility and helper methods to be used in controllers.
"""
import math
import numbers
from datetime import datetime
from dictalchemy import asdict
from knoweak import app_constants
from knoweak.errors import build_error, Message


def get_collection_page(req, query, asdict_func=None):
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
    :param asdict_func: (Optional) Custom function to make a dict from a model.
        When informed, overrides the default behavior.
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

    # Setup asdict_proxy to get a dict from each result item and build response
    asdict_proxy = asdict_func or asdict
    data = [asdict_proxy(record) for record in records]
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


def validate_number(field_name, field_value, is_mandatory=False,
                    min_value=None, max_value=None, exists_strategy=None):
    """Validates a number with general predefined rules.

    :param field_name: The field name to put in error object.
    :param field_value: The field value to be validated.
    :param is_mandatory: Indicates that the field is mandatory. That means that
        an error is returned if value is None.
        Default is false.
    :param min_value: Minimum value considered valid (inclusive).
        Default is None.
    :param max_value: Maximum value considered valid (inclusive).
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

    # Must be of one of numeric types
    if not isinstance(field_value, numbers.Number):
        return build_error(Message.ERR_FIELD_VALUE_MUST_BE_NUMBER, field_name=field_name)

    # Check min and/or max when requested
    if min_value and field_value < min_value:
        return build_error(Message.ERR_FIELD_VALUE_BELOW_MIN, field_name=field_name)
    if max_value and field_value > max_value:
        return build_error(Message.ERR_FIELD_VALUE_ABOVE_MAX, field_name=field_name)

    # Must be unique
    if exists_strategy and exists_strategy():
        return build_error(Message.ERR_FIELD_VALUE_ALREADY_EXISTS, field_name=field_name)


def validate_str(field_name, field_value, is_mandatory=False, min_length=None, max_length=None, exists_strategy=None):
    """Validates a string with general predefined rules.

    The string cannot be empty or contain any leading or trailing whitespace.
    This rule is always applied as long as the value of the field is informed
    and is a string.

    :param field_name: The field name to put in error object.
    :param field_value: The field value to be validated.
    :param is_mandatory: Indicates that the field is mandatory. That means that
        an error is returned if value is None.
        Default is false.
    :param min_length: Minimum length allowed. An error is returned if len(field_value)
        is below this value. When None, this validation will be skipped.
        Default is None.
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

    # Cannot be empty (general safe rule whether it's mandatory or not)
    if not field_value or field_value.isspace():
        return build_error(Message.ERR_FIELD_CANNOT_BE_EMPTY, field_name=field_name)

    # Prevent values with leading or trailing spaces
    if len(field_value) != len(field_value.strip()):
        return build_error(Message.ERR_FIELD_WITH_LEADING_OR_TRAILING_SPACES, field_name=field_name)

    # Length must be valid
    if min_length and len(field_value) < min_length:
        return build_error(Message.ERR_FIELD_MIN_LENGTH, field_name=field_name)
    if max_length and len(field_value) > max_length:
        return build_error(Message.ERR_FIELD_MAX_LENGTH, field_name=field_name)

    # Must be unique
    if exists_strategy and exists_strategy():
        return build_error(Message.ERR_FIELD_VALUE_ALREADY_EXISTS, field_name=field_name)


def patch_item(original_item, new_item, only=None):
    """Patches a dict object with another dict with matching fields.
    Original item will be updated in place.

    :param original_item: The item that should be patched.
    :param new_item: The item with patching data.
    :param only: A list of strings containing the name of specific fields to patch.
        Other fields will be ignored.
        Default: None
    :return: The patched item or None if the result of patch operation is equal
        to the ``original_item``.
    """
    old_item = original_item.asdict()
    original_item.fromdict(new_item, only=only)
    new_item = original_item.asdict()
    if new_item != old_item:
        if hasattr(original_item, 'last_modified_on'):
            original_item.last_modified_on = datetime.utcnow()
        return original_item
    return None
