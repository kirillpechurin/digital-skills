from portfolio.internal.biz.deserializers.base_deserializer import BaseDeserializer
from portfolio.internal.biz.deserializers.children import DES_FROM_DB_INFO_CHILDREN, ChildrenDeserialize
from portfolio.models.children_organisation import ChildrenOrganisation

DES_FROM_DB_LIST_LEARNERS = 'des-from-db-list-learners'


class ChildrenOrganisationDeserializer(BaseDeserializer):

    @classmethod
    def _get_deserializer(cls, format_des: str):
        if format_des == DES_FROM_DB_LIST_LEARNERS:
            return cls._des_from_db_list_learners
        else:
            raise TypeError

    @staticmethod
    def _des_from_db_list_learners(data):
        return [
            ChildrenOrganisation(
                id=row['children_organisation_id'],
                children=ChildrenDeserialize.deserialize(row, DES_FROM_DB_INFO_CHILDREN)
            )
            for row in data
        ]
