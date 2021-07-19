from portfolio.internal.biz.dao.parents import ParentsDao
from portfolio.models.parents import Parents


class ParentsService:

    @staticmethod
    def get_by_account_id(account_main_id: int):
        parents, err = ParentsDao().get_by_account_id(account_main_id)
        if err:
            return None, err
        return parents, None
