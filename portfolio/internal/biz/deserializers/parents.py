from portfolio.internal.biz.deserializers.base_deserializer import BaseDeserializer
from portfolio.models.parents import Parents

DES_FROM_DB_INFO_PARENTS = 'des-from-db-info-parents'


class ParentsDeserializer(BaseDeserializer):

    @classmethod
    def _get_deserializer(cls, format_des: str):
        if format_des == DES_FROM_DB_INFO_PARENTS:
            return cls._deserializer_from_db_info_parents
        else:
            raise TypeError

    @staticmethod
    def _deserializer_from_db_info_parents(parents_dict):
        return Parents(
            id=parents_dict.get('parents_id'),
            name=parents_dict.get('parents_name'),
            surname=parents_dict.get('parents_surname'),
        )
