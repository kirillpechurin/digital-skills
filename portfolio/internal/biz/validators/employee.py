from marshmallow import Schema, fields


class AddEmployeeSchema(Schema):
    login = fields.Str(required=True)
    name = fields.Str(required=True)
    surname = fields.Str(required=True)
    specialty = fields.Str(required=True)


class EditEmployeeSchema(Schema):
    login = fields.Str(required=False, allow_none=False)
    name = fields.Str(required=False, allow_none=False)
    surname = fields.Str(required=False, allow_none=False)
    specialty = fields.Str(required=False, allow_none=False)
