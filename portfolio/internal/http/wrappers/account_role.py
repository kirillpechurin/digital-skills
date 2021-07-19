import json

from flask import request

from portfolio.internal.biz.services.account_role import AccountRoleService
from portfolio.models.account_role import AccountRole


def check_account_role(func):
    def wrapper(*args, **kwargs):
        if request.method == 'POST':
            if not request.form.get('role_id'):
                return json.dumps("Выберите роль")
            account_role = AccountRole(id=request.form.get('role_id'))
            account_role, err = AccountRoleService.get_name_by_id(account_role)
            if err:
                return json.dumps(err)
            response = func(*args, account_role_id=account_role.id, **kwargs)
            return response
        elif request.method == 'GET':
            list_account_role, err = AccountRoleService.get_all()
            if err:
                return json.dumps(err)

            response = func(*args, list_account_role=list_account_role, **kwargs)
            return response

    wrapper.__name__ = func.__name__
    return wrapper
