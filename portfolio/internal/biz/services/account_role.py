from portfolio.internal.biz.dao.account_role import AccountRoleDao
from portfolio.models.account_role import AccountRole


class AccountRoleService:

    @staticmethod
    def get_name_by_id(account_role: AccountRole):
        account_role, err = AccountRoleDao().get_by_id(account_role.id)
        if err:
            return None, err
        return account_role, None

    @staticmethod
    def get_all():
        list_account_role, err = AccountRoleDao().get_all()
        if err:
            return None, err
        return list_account_role, None
