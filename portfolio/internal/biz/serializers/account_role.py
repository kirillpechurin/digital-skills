from typing import List

from portfolio.internal.biz.serializers.base_serializer import BaseSerializer
from portfolio.models.account_role import AccountRole

SER_FOR_GET_REGISTER = 'ser-for-get-register'


class AccountRoleSerializer(BaseSerializer):

    @classmethod
    def _get_serializer(cls, format_ser: str):
        if format_ser == SER_FOR_GET_REGISTER:
            return cls._ser_for_get_register

    @staticmethod
    def _ser_for_get_register(list_account_role: List[AccountRole]):
        return [
            {
                "id": role.id,
                "name": role.name
            }
            for role in list_account_role
        ]
