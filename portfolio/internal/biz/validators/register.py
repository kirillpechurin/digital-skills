from marshmallow import Schema, fields


class RegisterParentSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    surname = fields.Str(required=True)
    repeat_password = fields.Str(required=True)


class RegisterOrganisationSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    name_organisation = fields.Str(required=True)
    email_organisation = fields.Email(required=True)
    password = fields.Str(required=True)
    repeat_password = fields.Str(required=True)
