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
    if lang == "pt-BR":
        return MessagePTBR[message_enum.name].value.format(message_args)
    return message_enum.value.format(message_args)


class Message(Enum):
    ERR_NO_CONTENT = "No content was received."
    ERR_INVALID_VALUE_TYPE = "Invalid value type."
    ERR_FIELD_CANNOT_BE_NULL = "Field must be informed."
    ERR_FIELD_CANNOT_BE_EMPTY = "Field cannot be empty."
    ERR_FIELD_VALUE_INVALID = "Field value is invalid."
    ERR_FIELD_VALUE_ALREADY_EXISTS = "Field value already exists."
    ERR_FIELD_VALUE_MUST_BE_STRING = "Field value must be a string."
    ERR_FIELD_MIN_LENGTH = "Field value length is below allowed limit (min. {} characters)."
    ERR_FIELD_MAX_LENGTH = "Field value length is above allowed limit (max. {} characters)."
    ERR_FIELD_WITH_LEADING_OR_TRAILING_SPACES = "Field value cannot contain leading or trailing spaces."
    ERR_FIELD_VALUE_MUST_BE_NUMBER = "Field value must be a number."
    ERR_FIELD_VALUE_ABOVE_MAX = "Number is above max value allowed (min. {})."
    ERR_FIELD_VALUE_BELOW_MIN = "Number is below min value allowed (max. {})."

    ERR_DEPARTMENT_ID_ALREADY_IN_ORGANIZATION = "Department already exists in organization informed."
    ERR_ORGANIZATION_SECURITY_THREAT_ID_INVALID = "Security threat id is invalid or doesn't exist in organization."
    ERR_NO_ITEMS_TO_ANALYZE = "No items to analyze."


class MessagePTBR(Enum):
    ERR_NO_CONTENT = "Nenhum conteúdo recebido."
    ERR_INVALID_VALUE_TYPE = "O tipo do valor é inválido."
    ERR_FIELD_CANNOT_BE_NULL = "O campo é obrigatório."
    ERR_FIELD_CANNOT_BE_EMPTY = "O campo não pode estar vazio."
    ERR_FIELD_VALUE_INVALID = "O valor do campo é inválido."
    ERR_FIELD_VALUE_ALREADY_EXISTS = "O valor informado já existe."
    ERR_FIELD_VALUE_MUST_BE_STRING = "O valor deve ser um texto."
    ERR_FIELD_MIN_LENGTH = "O texto é mais curto do que o permitido (mín. {} caracteres)."
    ERR_FIELD_MAX_LENGTH = "O texto é mais longo do que o permitido (máx. {} caracteres)."
    ERR_FIELD_WITH_LEADING_OR_TRAILING_SPACES = "O texto não pode conter espaços no início ou no fim."
    ERR_FIELD_VALUE_MUST_BE_NUMBER = "O valor do campo deve ser um número."
    ERR_FIELD_VALUE_ABOVE_MAX = "O número informado está acima do valor máximo permitido (mín. {})."
    ERR_FIELD_VALUE_BELOW_MIN = "O número informado está abaixo do valor mínimo permitido (máx. {})."

    ERR_DEPARTMENT_ID_ALREADY_IN_ORGANIZATION = "O departamento já existe na organização."
    ERR_ORGANIZATION_SECURITY_THREAT_ID_INVALID = "O identificador da ameaça é inválido ou não existe na organização."
    ERR_NO_ITEMS_TO_ANALYZE = "Nenhum item a ser analisado."
