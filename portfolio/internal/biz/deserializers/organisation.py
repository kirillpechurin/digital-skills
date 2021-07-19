from portfolio.internal.biz.deserializers.base_deserializer import BaseDeserializer
from portfolio.models.organisation import Organisation

DES_FROM_DB_ALL_ORGANISATIONS = 'des-from-db-full-organisation'


class OrganisationDeserializer(BaseDeserializer):

    @classmethod
    def _get_deserializer(cls, format_des: str):
        if format_des == DES_FROM_DB_ALL_ORGANISATIONS:
            return cls._des_from_db_all_organisation

    @staticmethod
    def _des_from_db_all_organisation(data):
        return [
            Organisation(
                id=data[i]['organisation_id'],
                name=data[i]['organisation_name'],
                login=data[i]['organisation_login'],
                photo_link=data[i]['organisation_photo_link'],
                description=data[i]['organisation_description']
            )
            for i in range(len(data))
        ]
