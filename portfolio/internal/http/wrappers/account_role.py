import json

from flask import request, session

from portfolio.internal.biz.services.account_role import AccountRoleService
from portfolio.internal.biz.services.auth_service import AuthService
from portfolio.models.account_role import AccountRole
from portfolio.models.account_session import AccountSession


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


def check_account_role_organisation_and_login_required(func):
    def wrapper(*args, **kwargs):
        if not session.get('auth-token'):
            return "Где токен?"

        session_id = AccountSession.get_session_id_from_token(session.get('auth-token'))
        if not session_id:
            return "Невалидный или недействительный токен"

        account_main, err = AuthService.get_account_main_by_session_id_with_confirmed(session_id)
        if err:
            return "HZ"

        if not account_main:
            return "Невалидный или недействительный токен"

        if not account_main.is_confirmed:
            return "Пожалуйста, подтвердите email"

        account_role_id = AccountRole.get_account_role_from_token(session.get('auth-token'))

        if not account_role_id:
            return "Невалидный или устаревший токен"

        if account_role_id != 1:
            return "Недостаточно прав"
        response = func(*args, *kwargs)
        return response
    wrapper.__name__ = func.__name__
    return wrapper


def check_account_role_parents_and_login_required(func):
    def wrapper(*args, **kwargs):
        if not session.get('auth-token'):
            return "Где токен?"

        session_id = AccountSession.get_session_id_from_token(session.get('auth-token'))
        if not session_id:
            return "Невалидный или недействительный токен"

        account_main, err = AuthService.get_account_main_by_session_id_with_confirmed(session_id)
        if err:
            return "HZ"

        if not account_main:
            return "Невалидный или недействительный токен"

        if not account_main.is_confirmed:
            return "Пожалуйста, подтвердите email"

        account_role_id = AccountRole.get_account_role_from_token(session.get('auth-token'))

        if not account_role_id:
            return "Невалидный или устаревший токен"

        if account_role_id != 2:
            return "Недостаточно прав"

        response = func(*args, auth_account_main_id=account_main.id, **kwargs)
        return response
    wrapper.__name__ = func.__name__
    return wrapper
