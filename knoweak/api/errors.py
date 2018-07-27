"""
Error code definitions and helper methods.
"""
from enum import Enum


def build_error(message_enum, message_args=None, field_name=None, lang="pt-BR"):
    return {
        'code': message_enum.name,
        'message': get_message(message_enum, message_args, lang),
        'field': field_name
    }


def get_message(message_enum, message_args, lang):
    return message_enum.value.format(message_args)


class Message(Enum):
    ERR_NO_CONTENT = "No content was received."
    ERR_INVALID_VALUE_TYPE = "Invalid value type."
    ERR_FIELD_CANNOT_BE_NULL = "Field must be informed."
    ERR_FIELD_CANNOT_BE_EMPTY = "Field cannot be empty."
    ERR_FIELD_VALUE_INVALID = "Field value is invalid."
    ERR_FIELD_VALUE_ALREADY_EXISTS = "Field value already exists."
    ERR_FIELD_VALUE_MUST_BE_STRING = "Field value must be a string."
    ERR_FIELD_MIN_LENGTH = "Field value length is below allowed limit."
    ERR_FIELD_MAX_LENGTH = "Field value length is above allowed limit."
    ERR_FIELD_WITH_LEADING_OR_TRAILING_SPACES = "Field value cannot contain leading and/or trailing spaces."
    ERR_FIELD_VALUE_MUST_BE_NUMBER = "Field value must be a number."
    ERR_FIELD_VALUE_ABOVE_MAX = "Number is above max value allowed."
    ERR_FIELD_VALUE_BELOW_MIN = "Number is below min value allowed."

    ERR_TAX_ID_CANNOT_BE_NULL = "Tax ID must be informed."
    ERR_TAX_ID_MAX_LENGTH = "Tax ID length is above allowed limit."
    ERR_TAX_ID_ALREADY_EXISTS = "Tax ID already exists."
    ERR_LEGAL_NAME_CANNOT_BE_NULL = "Legal name must be informed."
    ERR_LEGAL_NAME_MAX_LENGTH = "Legal name length is above allowed limit."
    ERR_TRADE_NAME_MAX_LENGTH = "Trade name length is above allowed limit."
    ERR_DEPARTMENT_ID_CANNOT_BE_NULL = "Department identifier must be informed."
    ERR_DEPARTMENT_ID_INVALID = "Invalid department id."
    ERR_DEPARTMENT_ID_ALREADY_IN_ORGANIZATION = "Department already exists in organization informed."
    ERR_NAME_CANNOT_BE_NULL = "Name must be informed."
    ERR_NAME_CANNOT_BE_EMPTY = "Name cannot be empty."
    ERR_NAME_MAX_LENGTH = "Name length is above allowed limit."
    ERR_NAME_ALREADY_EXISTS = "Name already exists."
    ERR_DESCRIPTION_MAX_LENGTH = "Description length is above allowed limit."
    ERR_IT_ASSET_CATEGORY_ID_CANNOT_BE_NULL = "IT asset category id must be informed."
    ERR_IT_ASSET_CATEGORY_ID_ALREADY_EXISTS = "IT asset category id already exists."
    ERR_IT_ASSET_CATEGORY_ID_INVALID = "Invalid IT asset category id."
    ERR_ORGANIZATION_SECURITY_THREAT_ID_INVALID = "Security threat id is invalid or doesn't exist in organization."
