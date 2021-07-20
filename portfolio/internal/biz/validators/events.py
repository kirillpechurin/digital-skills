from marshmallow import Schema, fields

from portfolio.internal.biz.validators.utils import date_validate


class AddEventSchema(Schema):
    type = fields.Str(required=True, error_messages={'required': 'Это обязательное поле'})
    name = fields.Str(required=True, error_messages={'required': 'Это обязательное поле'})
    date_event = fields.Date(required=True, error_messages={'required': 'Это обязательное поле'}, validate=date_validate)
    event_hours = fields.Int(required=True, error_messages={'required': 'Это обязательное поле'})
    skill = fields.Str(required=True, error_messages={'required': 'Это обязательное поле'})


class EditEventSchema(Schema):
    type = fields.Str(required=False, allow_none=True)
    name = fields.Str(required=False, allow_none=True)
    date_event = fields.Str(required=False)
    hours = fields.Int(required=False, allow_none=True)
    skill = fields.Str(required=False, allow_none=True)
