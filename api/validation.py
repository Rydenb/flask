"""
Shared input validation for the SDRM endpoints (services, volunteer, contact, newsletter).
Each helper raises ValidationError naming the offending field; endpoints turn that into a 400.
"""
import re
from flask import request


EMAIL_PATTERN = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')
PHONE_PATTERN = re.compile(r'^[0-9+\-().\s]+$')


class ValidationError(Exception):
    """Invalid client input. Carries the field name so the frontend can highlight it."""
    def __init__(self, field, message):
        super().__init__(message)
        self.field = field
        self.message = message

    def response(self):
        return {'message': self.message, 'field': self.field}, 400


def get_json_body():
    """Return the request body as a dict, or raise if it is missing or not a JSON object"""
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        raise ValidationError('body', 'Request body must be a JSON object')
    return data


def clean_string(data, field, max_length, required=True):
    """Return data[field] stripped, None if optional and blank, or raise"""
    value = data.get(field)
    if value is None or (isinstance(value, str) and not value.strip()):
        if required:
            raise ValidationError(field, f'{field} is required')
        return None
    if not isinstance(value, str):
        raise ValidationError(field, f'{field} must be a string')
    value = value.strip()
    if len(value) > max_length:
        raise ValidationError(field, f'{field} must be {max_length} characters or fewer')
    return value


def clean_email(data, field='email'):
    """Return a lowercased, format-checked email address, or raise"""
    value = clean_string(data, field, 254)
    if not EMAIL_PATTERN.match(value):
        raise ValidationError(field, f'{field} must be a valid email address')
    return value.lower()


def clean_phone(data, field='phone'):
    """Return an optional phone number with 7-15 digits, or raise"""
    value = clean_string(data, field, 30, required=False)
    if value is None:
        return None
    digits = re.sub(r'\D', '', value)
    if not PHONE_PATTERN.match(value) or not 7 <= len(digits) <= 15:
        raise ValidationError(field, f'{field} must be a valid phone number')
    return value


def clean_choice(value, field, choices):
    """Return value lowercased if it is one of choices, None if blank, or raise"""
    if value is None or not value.strip():
        return None
    value = value.strip().lower()
    if value not in choices:
        raise ValidationError(field, f'{field} must be one of: {", ".join(choices)}')
    return value
