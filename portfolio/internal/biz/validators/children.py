from marshmallow import fields, Schema

from portfolio.internal.biz.validators.utils import date_validate


class AddChildrenSchema(Schema):
    name = fields.Str(required=True, error_messages={'required': 'Это обязательное поле'})
    surname = fields.Str(required=True, error_messages={'required': 'Это обязательное поле'})
    date_born = fields.Date(required=True, error_messages={'required': 'Это обязательное поле'}, validate=date_validate)


class EditChildSchema(Schema):
    name = fields.Str(required=False, allow_none=False, error_messages={'required': 'Это обязательное поле'})
    surname = fields.Str(required=False, allow_none=False, error_messages={'required': 'Это обязательное поле'})
    date_born = fields.Date(required=False, allow_none=False, error_messages={'required': 'Это обязательное поле'}, validate=date_validate)
