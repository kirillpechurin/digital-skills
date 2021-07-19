from flask import json

from portfolio.internal.biz.services.organisation import OrganisationService
from portfolio.internal.http.wrappers.auth import required_auth_with_confirmed_email
from portfolio.models.account_main import AccountMain


def get_org_id_and_acc_id_with_confirmed_email(func):
    @required_auth_with_confirmed_email
    def wrapper(*args, auth_account_main_id: int, **kwargs):
        account_main = AccountMain(id=auth_account_main_id)

        organisation, err = OrganisationService.get_by_account_id(account_main.id)
        if err:
            return json.dumps(err)

        response = func(*args, auth_account_main_id=account_main.id, organisation_id=organisation.id, **kwargs)
        return response

    wrapper.__name__ = func.__name__
    return wrapper
