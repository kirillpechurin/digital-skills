from marshmallow import Schema, fields


def validate_code(value: str):
    if len(value) != 6 or not value.isdigit():
        raise TypeError


class ConfirmCodeSchema(Schema):
    code = fields.Str(required=True, error_messages={'required': 'Обязательное поле'}, validate=validate_code)
