from portfolio.internal.biz.deserializers.base_deserializer import BaseDeserializer
from portfolio.models.children import Children
from portfolio.models.parents import Parents

DES_FROM_DB_INFO_CHILDREN = 'des-from-db-info-children'
DES_FROM_DB_INFO_CHILD = 'des-from-db-info-child'
DES_FOR_ADD_CHILD = 'des-for-add-child'

class ChildrenDeserialize(BaseDeserializer):

    @classmethod
    def _get_deserializer(cls, format_des: str):
        if format_des == DES_FROM_DB_INFO_CHILDREN:
            return cls._des_from_db_info_children
        elif format_des == DES_FROM_DB_INFO_CHILD:
            return cls._des_from_db_info_child
        elif format_des == DES_FOR_ADD_CHILD:
            return cls._des_for_add_child
        else:
            raise TypeError

    @staticmethod
    def _des_from_db_info_children(list_children):
        return [
            Children(
                id=child.get('children_id'),
                name=child.get('children_name'),
                surname=child.get('children_surname'),
                date_born=child.get('children_date_born'),
                parents=Parents(
                    id=child.get('children_parents_id')
                )
            )
            for child in list_children
        ]

    @staticmethod
    def _des_from_db_info_child(row) -> Children:
        return Children(
            id=row.get('children_id'),
            name=row.get('children_name'),
            surname=row.get('children_surname'),
            date_born=row.get('children_date_born')
        )

    @staticmethod
    def _des_for_add_child(child_dict) -> Children:
        return Children(
            name=child_dict.get('name'),
            surname=child_dict.get('surname'),
            date_born=child_dict.get('date_born')
        )
