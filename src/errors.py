"""
Error code definitions and helper methods.
"""
from enum import Enum


def get_message(message_enum, lang):
    return message_enum.value


def build_error(message_enum, lang="pt-BR", field_name=None):
    return {
        'code': message_enum.name,
        'message': get_message(message_enum, lang)
    }


class Message(Enum):
    ERR_NO_CONTENT = "No content was received."
    ERR_TAX_ID_CANNOT_BE_NULL = "Tax ID cannot be null."
    ERR_TAX_ID_MAX_LENGTH = "Tax ID length is above allowed limit."
    ERR_TAX_ID_ALREADY_EXISTS = "Tax ID already exists."
    ERR_LEGAL_NAME_CANNOT_BE_NULL = "Legal name cannot be null."
    ERR_LEGAL_NAME_MAX_LENGTH = "Legal name length is above allowed limit."
    ERR_TRADE_NAME_MAX_LENGTH = "Trade name length is above allowed limit."
    ERR_DEPARTMENT_ID_NOT_FOUND = "Department requested not found."
    ERR_NAME_CANNOT_BE_NULL = "Name cannot be null"
    ERR_NAME_MAX_LENGTH = "Name length is above allowed limit."
    ERR_NAME_ALREADY_EXISTS = "Name already exists."
    ERR_DESCRIPTION_MAX_LENGTH = "Description length is above allowed limit."
    ERR_IT_ASSET_CATEGORY_ID_CANNOT_BE_NULL = "IT asset category id cannot be null."
    ERR_INVALID_IT_ASSET_CATEGORY_ID = "Invalid IT asset category id."
