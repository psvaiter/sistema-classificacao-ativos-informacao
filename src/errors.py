"""
Error code definitions.
"""
from enum import Enum


class Message(Enum):
    ERR_TAX_ID_MANDATORY = "Tax ID is mandatory."
    ERR_TAX_ID_MAX_LENGTH = "Tax ID length is above allowed limit."
    ERR_TAX_ID_ALREADY_EXISTS = "Tax ID already exists."
    ERR_LEGAL_NAME_MANDATORY = "Legal name is mandatory."
    ERR_LEGAL_NAME_MAX_LENGTH = "Legal name length is above allowed limit."
    ERR_TRADE_NAME_MAX_LENGTH = "Trade name length is above allowed limit."
