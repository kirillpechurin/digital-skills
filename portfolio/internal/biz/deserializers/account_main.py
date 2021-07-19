from portfolio.internal.biz.deserializers.base_deserializer import BaseDeserializer
from portfolio.models.account_main import AccountMain
from portfolio.models.account_role import AccountRole

DES_FROM_REGISTER = "des-from-register"
DES_FROM_LOGIN= "des-from-login"
DES_FROM_DB_ACCOUNT_MAIN_DETAIL = "des-from-db-account-main-detail"


class AccountMainDeserializer(BaseDeserializer):

    @classmethod
    def _get_deserializer(cls, format_des: str):
        if format_des == DES_FROM_REGISTER:
            return cls._des_from_register
        elif format_des == DES_FROM_LOGIN:
            return cls._des_from_login
        elif format_des == DES_FROM_DB_ACCOUNT_MAIN_DETAIL:
            return cls._des_from_db_account_main_detail
        else:
            raise TypeError

    @staticmethod
    def _des_from_register(account_main_dict):
        return AccountMain(
            name=account_main_dict.get('name'),

        )

    @staticmethod
    def _des_from_login(account_main_dict):
        return AccountMain(
            password=account_main_dict.get('password'),
            email=account_main_dict.get('email')
        )

    @staticmethod
    def _des_from_db_account_main_detail(row):
        return AccountMain(
            id=row.get('account_main_id'),
            created_at=row.get('account_main_created_at'),
            edited_at=row.get('account_main_edited_at'),
            email=row.get('account_main_email'),
            name=row.get('account_main_name'),
            hash_password=row.get('account_main_password'),
            account_role=AccountRole(id=row.get('account_main_account_role_id')),
            is_confirmed=row.get('account_main_is_confirmed'),
        )
