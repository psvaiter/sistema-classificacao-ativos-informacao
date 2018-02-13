import six
import datetime
import decimal
from uuid import UUID

import falcon
import falcon.errors
from falcon.media import BaseHandler
from falcon.util import json
import inflection


class HTTPUnprocessableEntity(falcon.HTTPUnprocessableEntity):
    """
    This class adds support to send multiple errors at once in response.
    See documentation for base class for more details.
    """

    def __init__(self, errors=None, **kwargs):
        super().__init__(**kwargs)
        self.errors = None

        if isinstance(errors, list):
            self.errors = errors

    def to_dict(self, obj_type=dict):
        """
        Override to include 'errors' in response.
        See base class implementation for details.
        """

        obj = super().to_dict(obj_type)

        if isinstance(self.errors, list):
            obj['errors'] = self.errors

        return obj


class JSONHandler(BaseHandler):
    """Handler built using Python's :py:mod:`json` module."""

    def __init__(self, contract_in_camel_case=False):
        self.contract_in_camel_case = contract_in_camel_case

    def deserialize(self, raw):
        try:
            obj = json.loads(raw.decode('utf-8'))
            if self.contract_in_camel_case:
                obj = self.snake_case_keys(obj)
            return obj
        except ValueError as err:
            raise falcon.errors.HTTPBadRequest(
                'Invalid JSON',
                'Could not parse JSON body - {0}'.format(err)
            )

    def serialize(self, obj):
        if self.contract_in_camel_case:
            obj = self.camel_case_keys(obj)
        result = json.dumps(obj, ensure_ascii=False, default=self.extended_encoder)
        if six.PY3 or not isinstance(result, bytes):
            return result.encode('utf-8')

        return result

    @classmethod
    def extended_encoder(cls, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        if isinstance(obj, UUID):
            return str(obj)

    @classmethod
    def camel_case_keys(cls, obj):
        """
        Converts object keys expected to be in snake_case to camelCase.

        :param obj: Object to be converted.
        :return: A new object of the same type (dict or list) with keys
            converted to camel case. If ``obj`` is not a dict or a list
            the ``obj`` is returned unchanged.
        """

        # Camel case keys of object provided
        if isinstance(obj, dict):
            new_dictionary = {}
            for (key, value) in obj.items():
                if isinstance(key, str):
                    key = cls.camel_case(key)
                new_dictionary[key] = cls.camel_case_keys(value)
            return new_dictionary

        # If obj is a list it MAY contain objects to be camel cased
        if isinstance(obj, list):
            new_list = []
            for element in obj:
                new_list.append(cls.camel_case_keys(element))
            return new_list

        # Nothing to camel case so return as is
        return obj

    @classmethod
    def camel_case(cls, text):
        """
        Converts text expected to be in snake_case to camelCase.
        Examples:
            "sample_text" becomes "sampleText"
            "SomE_oTHER_Text" becomes "someOtherText"

        :param text: The text to be converted.
        :return: A new string with text in camelCase.
        """
        words = text.split('_')
        if words:
            first_word = words[0].lower()
            capitalized_words = [word.capitalize() for word in words[1:]]
            camel_cased_text = first_word + ''.join(capitalized_words)
            return camel_cased_text
        return text

    @classmethod
    def snake_case_keys(cls, obj):
        """
        Converts object keys expected to be in camelCase to snake_case.

        :param obj: Object to be converted.
        :return: A new object of the same type (dict or list) with keys
            converted to snake_case. If ``obj`` is not a dict or a list
            the ``obj`` is returned unchanged.
        """

        # Snake case keys of object provided
        if isinstance(obj, dict):
            new_dictionary = {}
            for (key, value) in obj.items():
                if isinstance(key, str):
                    key = inflection.underscore(key)
                new_dictionary[key] = cls.snake_case_keys(value)
            return new_dictionary

        # If obj is a list it MAY contain objects to be snake cased
        if isinstance(obj, list):
            new_list = []
            for element in obj:
                new_list.append(cls.snake_case_keys(element))
            return new_list

        # Nothing to snake case so return as is
        return obj
