import json
from typing import List

from flask import Blueprint, request, make_response, render_template, url_for, session, flash
from sqlalchemy import select
from werkzeug.utils import redirect

from portfolio.internal.biz.deserializers.account_main import DES_FROM_REGISTER, AccountMainDeserializer, DES_FROM_LOGIN
from portfolio.internal.biz.services.account_main import AccountMainService
from portfolio.internal.biz.services.auth_service import AuthService
from portfolio.internal.biz.validators.confirm_code import ConfirmCodeSchema
from portfolio.internal.biz.validators.login import LoginAuthSchema
from portfolio.internal.biz.validators.password import EditPasswordSchema
from portfolio.internal.biz.validators.register import RegisterOrganisationSchema, RegisterParentSchema
from portfolio.internal.http.wrappers.account_role import check_account_role
from portfolio.internal.http.wrappers.auth import required_auth, required_auth_with_confirmed_email
from portfolio.models.account_main import AccountMain
from portfolio.models.account_role import AccountRole
from portfolio.models.auth_code import AuthCode
from portfolio.models.organisation import Organisation
from portfolio.models.parents import Parents

account = Blueprint('account', __name__, template_folder='account', static_folder='/account')


@account.route("/register", methods=['GET', 'POST'])
@check_account_role
def register(account_role_id: int = None,
             list_account_role: List[AccountRole] = None):
    if request.method == 'POST':
        organisation = None
        parent = None
        if account_role_id == 1:  # Organisation
            errors = RegisterOrganisationSchema().validate(dict(
                name=request.form.get('name'),
                email=request.form.get('email'),
                password=request.form.get('password'),
                name_organisation=request.form.get('name_organisation'),
                email_organisation=request.form.get('email_organisation'),
                repeat_password=request.form.get('repeat_password')
            ))
            organisation = Organisation(name=request.form.get('name_organisation'),
                                        login=request.form.get('email_organisation'))
        elif account_role_id == 2:  # Parent
            errors = RegisterParentSchema().validate(dict(
                surname=request.form.get('surname'),
                repeat_password=request.form.get('repeat_password'),
                name=request.form.get('name'),
                email=request.form.get('email'),
                password=request.form.get('password'),
            ))
            parent = Parents(name=request.form.get('name'),
                             surname=request.form.get('surname'))
        else:
            errors = NotImplementedError
        if errors:
            return json.dumps(errors)

        account_main = AccountMainDeserializer.deserialize(request.form, DES_FROM_REGISTER)
        account_main.account_role = AccountRole(id=account_role_id)
        if organisation:
            organisation.account_main = account_main
        if parent:
            parent.account_main = account_main
        account_main, errors = AuthService.register(account_main, organisation, parent)
        if errors:
            return json.dumps(errors)
        if account_main.is_confirmed:
            return redirect(url_for('account.detail'))
        return render_template('account/registration.html',
                               context={"is_email_sent": account_main.is_email_sent})

    elif request.method == 'GET':
        return make_response(
            render_template(
                'account/registration.html',
                context={"roles": list_account_role}
            )
        )


@account.route('/auth/code', methods=['POST'])
def confirm_code():
    validate_errors = ConfirmCodeSchema().validate(dict(code=request.form.get('code')))
    if validate_errors:
        return json.dumps(validate_errors)

    auth_code = AuthCode(code=request.form.get('code'))
    _, err = AuthService.confirm_code(auth_code)
    if err:
        return json.dumps(err)

    return redirect(url_for('account.login'))


@account.route("/detail", methods=['GET'])
@required_auth
def get_detail_info(auth_account_main_id: int):
    account_main, err = AccountMainService.get_detail_account_info(auth_account_main_id)
    if err:
        return json.dumps(err)

    response = make_response(render_template(
        'account/detail.html',
        account_main=account_main
    ))
    response.status_code = 200
    return response


@account.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        errors = LoginAuthSchema().validate(dict(email=request.form['email'],
                                                 password=request.form['password']))
        if errors:
            return json.dumps(errors)

        account_main = AccountMainDeserializer.deserialize(request.form, DES_FROM_LOGIN)
        account_main, err = AuthService.auth_login(account_main)
        if err:
            return json.dumps(err)
        session['auth-token'] = account_main.auth_token
        return redirect(url_for('account.get_detail_info'))
    return render_template('account/login.html', errors=None)


@account.route('/edit_password', methods=['GET', 'POST'])
@required_auth_with_confirmed_email
def edit_password(auth_account_main_id: int):
    if request.method == "POST":
        errors = EditPasswordSchema().validate(dict(
            old_password=request.form['old_password'],
            new_password=request.form['new_password'],
            repeat_new_password=request.form['repeat_new_password']
        ))
        if errors:
            return json.dumps(errors)
        if request.form['new_password'] != request.form['repeat_new_password']:
            return json.dumps('Пароли не одинаковы')
        account_main = AccountMain(id=auth_account_main_id, password=request.form['new_password'])
        account_main, err = AuthService.update_password(request.form['old_password'], account_main)
        if err:
            return json.dumps(err)
        flash('Успешно обновили пароль')
        resp = make_response(
            redirect(
                url_for('account.get_detail_info')
            )
        )
        return resp
