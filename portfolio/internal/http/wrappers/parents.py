from flask import json

from portfolio.internal.biz.services.children_service import ChildrenService
from portfolio.internal.biz.services.parents import ParentsService
from portfolio.internal.http.wrappers.auth import required_auth_with_confirmed_email
from portfolio.models.account_main import AccountMain
from portfolio.models.children import Children
from portfolio.models.parents import Parents


def get_parent_id_and_acc_id_with_confirmed_email(func):
    @required_auth_with_confirmed_email
    def wrapper(*args, auth_account_main_id: int, **kwargs):
        account_main = AccountMain(id=auth_account_main_id)

        parent, err = ParentsService.get_by_account_id(account_main.id)
        if err:
            return json.dumps(err)

        response = func(*args, auth_account_main_id=account_main.id, parent_id=parent.id, **kwargs)
        return response
    wrapper.__name__ = func.__name__
    return wrapper


def check_child_by_parent(func):
    @get_parent_id_and_acc_id_with_confirmed_email
    def wrapper(*args, auth_account_main_id: int, parent_id: int, **kwargs):
        children = Children(
            parents=Parents(
                id=parent_id,
                account_main=AccountMain(id=auth_account_main_id)
            )
        )

        list_children, err = ChildrenService.get_children_by_parents_id(children)
        if err:
            return json.dumps(err)
        response = func(*args, list_children=list_children, parent_id=list_children[0].parents.id, **kwargs)
        return response
    wrapper.__name__ = func.__name__
    return wrapper
