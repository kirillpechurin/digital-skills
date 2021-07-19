
from flask import Blueprint, request, json, url_for, redirect, make_response, render_template, flash

from portfolio.internal.biz.services.organisation import OrganisationService
from portfolio.internal.http.wrappers.parents import get_parent_id_and_acc_id_with_confirmed_email

main = Blueprint('main', __name__, template_folder='templates/main', static_folder='static/main')


@main.route('/organisations', methods=['GET'])
@get_parent_id_and_acc_id_with_confirmed_email
def list_organisation(auth_account_main_id: int, parent_id: int):
    if request.method == 'GET':

        organisations, err = OrganisationService.get_all_organisations()

        if err:
            return json.dumps(err)
        response = make_response(render_template(
            'main/list_organisations.html',
            organisations=organisations
        ))
        return response
