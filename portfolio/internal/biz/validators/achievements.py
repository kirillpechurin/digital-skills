from marshmallow import Schema, fields


class AddAchievementSchema(Schema):
    name = fields.Str(required=True, error_messages={'required': 'Это обязательное поле'})
    nomination = fields.Str(required=True, error_messages={'required': 'Это обязательное поле'})
    points = fields.Integer(required=True, error_messages={'required': 'Это обязательное поле'})


class EditAchievementSchema(Schema):
    name = fields.Str(required=False, allow_none=True)
    nomination = fields.Str(required=False, allow_none=True)
    points = fields.Integer(required=False, allow_none=True)
