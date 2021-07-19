from portfolio.internal.biz.deserializers.base_deserializer import BaseDeserializer
from portfolio.models.organisation import Organisation

DES_FROM_DB_ALL_ORGANISATIONS = 'des-from-db-all-organisations'
DES_FROM_DB_DETAIL_ORGANISATION = 'des-from-db-detail-organisation'


class OrganisationDeserializer(BaseDeserializer):

    @classmethod
    def _get_deserializer(cls, format_des: str):
        if format_des == DES_FROM_DB_ALL_ORGANISATIONS:
            return cls._des_from_db_all_organisation
        elif format_des == DES_FROM_DB_DETAIL_ORGANISATION:
            return cls._des_from_db_detail_organisation
        else:
            raise TypeError

    @staticmethod
    def _des_from_db_all_organisation(data):
        return [
            Organisation(
                id=row.get('organisation_id'),
                name=row.get('organisation_name'),
                login=row.get('organisation_login'),
                photo_link=row.get('organisation_photo_link'),
                description=row.get('organisation_description'),
            )
            for row in data
        ]

    @staticmethod
    def _des_from_db_detail_organisation(row):
        return Organisation(
                id=row.get('organisation_id'),
                name=row.get('organisation_name'),
                login=row.get('organisation_login'),
                photo_link=row.get('organisation_photo_link'),
                description=row.get('organisation_description'),
            )
