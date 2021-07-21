from portfolio.internal.biz.serializers.base_serializer import BaseSerializer
from portfolio.models.account_main import AccountMain


SER_FOR_REGISTER = "ser-for-register"
SER_FOR_DETAIL_ACCOUNT = "ser-for-detail-account"


class AccountMainSerializer(BaseSerializer):

    @classmethod
    def _get_serializer(cls, format_ser: str):
        if format_ser == SER_FOR_REGISTER:
            return cls._ser_for_register
        elif format_ser == SER_FOR_DETAIL_ACCOUNT:
            return cls._ser_for_detail_account

    @staticmethod
    def _ser_for_register(account_main: AccountMain):
        return {
            "id": account_main.id,
            "created_at": account_main.created_at,
            "edited_at": account_main.edited_at,
            "email": account_main.email,
            "name": account_main.name,
            "account_role": {
                "id": account_main.account_role.id
            },
            "is_email_sent": account_main.is_email_sent,
            "auth_token": account_main.auth_token,
        }

    @staticmethod
    def _ser_for_detail_account(account_main: AccountMain):
        return {
            "id": account_main.id,
            "email": account_main.email,
            "name": account_main.name,
            "account_role": {
                "id": account_main.account_role.id
            },
            "is_confirmed": account_main.is_confirmed,
        }
