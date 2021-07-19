from flask import Blueprint
from sqlalchemy import select

from portfolio.models.account_main import AccountMain

account = Blueprint('account', __name__, template_folder='account', static_folder='/account')


@account.route("/register")
def register():
    res = select(AccountMain)
    print(res)
    return 'hello world!'
