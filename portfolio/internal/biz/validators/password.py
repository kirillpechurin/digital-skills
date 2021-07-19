from marshmallow import Schema, fields


class RecoveryPasswordSchema(Schema):
    name = fields.Str(required=True, error_messages={'required': 'Обязательное поле'})
    email = fields.Email(required=True, error_messages={'required': 'Обязательное поле'})


class EditPasswordSchema(Schema):
    old_password = fields.Str(required=True, error_messages={"required": "Это обязательное поле"})
    new_password = fields.Str(required=True, error_messages={"required": "Это обязательное поле"})
    repeat_new_password = fields.Str(required=True, error_messages={"required": "Это обязательное поле"})
