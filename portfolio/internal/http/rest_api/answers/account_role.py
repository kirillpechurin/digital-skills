from typing import List

from flask import jsonify

from portfolio.internal.biz.serializers.account_role import AccountRoleSerializer, SER_FOR_GET_REGISTER
from portfolio.models.account_role import AccountRole


def get_response_get_register(list_account_role: List[AccountRole]):
    return jsonify(AccountRoleSerializer.serialize(list_account_role, SER_FOR_GET_REGISTER))
