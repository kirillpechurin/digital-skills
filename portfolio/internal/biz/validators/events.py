from marshmallow import Schema, fields

from portfolio.internal.biz.validators.utils import date_validate


class AddEventSchema(Schema):
    type = fields.Str(required=True, error_messages={'required': 'Это обязательное поле'})
    name = fields.Str(required=True, error_messages={'required': 'Это обязательное поле'})
    date_event = fields.Date(required=True, error_messages={'required': 'Это обязательное поле'}, validate=date_validate)
    event_hours = fields.Int(required=True, error_messages={'required': 'Это обязательное поле'})
    skill = fields.Str(required=True, error_messages={'required': 'Это обязательное поле'})
