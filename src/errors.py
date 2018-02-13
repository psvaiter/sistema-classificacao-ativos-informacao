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
    ERR_TAX_ID_MANDATORY = "Tax ID is mandatory."
    ERR_TAX_ID_MAX_LENGTH = "Tax ID length is above allowed limit."
    ERR_TAX_ID_ALREADY_EXISTS = "Tax ID already exists."
    ERR_LEGAL_NAME_MANDATORY = "Legal name is mandatory."
    ERR_LEGAL_NAME_MAX_LENGTH = "Legal name length is above allowed limit."
    ERR_TRADE_NAME_MAX_LENGTH = "Trade name length is above allowed limit."
