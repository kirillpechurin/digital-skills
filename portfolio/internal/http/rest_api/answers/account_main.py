from flask import jsonify

from portfolio.internal.biz.serializers.accounts import AccountMainSerializer, SER_FOR_REGISTER, SER_FOR_DETAIL_ACCOUNT
from portfolio.models.account_main import AccountMain


def get_response_register(account_main: AccountMain):
    return jsonify(AccountMainSerializer.serialize(account_main, SER_FOR_REGISTER))


def get_response_detail_info_account(account_main: AccountMain):
    return jsonify(AccountMainSerializer.serialize(account_main, SER_FOR_DETAIL_ACCOUNT))