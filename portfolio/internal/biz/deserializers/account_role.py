from typing import List

from internal.biz.deserializers.base_deserializer import BaseDeserializer
from models.account_role import AccountRole

SER_FOR_GET_LIST_ACCOUNT_ROLE = 'ser-for-get-list-account-role'


class AccountRoleDeserializer(BaseDeserializer):

    @classmethod
    def _get_deserializer(cls, format_des: str):
        if format_des == SER_FOR_GET_LIST_ACCOUNT_ROLE:
            return cls._ser_for_get_list_account_role
        else:
            raise TypeError

    @staticmethod
    def _ser_for_get_list_account_role(data) -> List[AccountRole]:
        return [
            AccountRole(
                id=row['account_role_id'],
                name=row['account_role_name']
            )
            for row in data
        ]
