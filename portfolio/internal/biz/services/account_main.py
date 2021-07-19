from portfolio.internal.biz.dao.account_main import AccountMainDao


class AccountMainService:

    @staticmethod
    def get_detail_account_info(account_main_id: int):
        account_main, err = AccountMainDao().get_by_id(account_main_id)
        if err:
            return None, err
        return account_main, None
