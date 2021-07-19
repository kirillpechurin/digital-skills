from typing import List

from portfolio.internal.biz.deserializers.base_deserializer import BaseDeserializer
from portfolio.models.account_role import AccountRole

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
                id=data[i]['account_role_id'],
                name=data[i]['account_role_name']
            )
            for i in range(len(data))
        ]
