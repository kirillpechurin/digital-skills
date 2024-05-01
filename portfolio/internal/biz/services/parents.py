from internal.biz.dao.parents import ParentsDao


class ParentsService:

    @staticmethod
    def get_by_account_id(account_main_id: int):
        parents, err = ParentsDao().get_by_account_id(account_main_id)
        if err:
            return None, err
        return parents, None
