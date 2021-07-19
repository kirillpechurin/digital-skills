from portfolio.internal.biz.dao.children import ChildrenDao
from portfolio.internal.biz.services.parents import ParentsService
from portfolio.models.children import Children


class ChildrenService:

    @staticmethod
    def get_children_by_parents_id(children: Children):
        parents, err = ParentsService.get_by_account_id(children.parents.account_main.id)
        if err:
            return None, err

        children.parents = parents

        list_children, err = ChildrenDao().get_all_by_parents_id(children)
        if err:
            return None, err
        return list_children, None
