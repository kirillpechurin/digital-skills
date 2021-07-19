
from flask import Blueprint, request, json, url_for, redirect, make_response, render_template, flash

from portfolio.internal.biz.services.employee import EmployeeService
from portfolio.internal.biz.services.events import EventsService
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


@main.route('/organisations/<int:organisation_id>', methods=['GET'])
@get_parent_id_and_acc_id_with_confirmed_email
def detail_organisation(auth_account_main_id: int, parent_id: int, organisation_id: int):
    if request.method == 'GET':
        organisation, err = OrganisationService.get_by_id(organisation_id)
        list_employee, err = EmployeeService.get_list_employee_by_org_id(organisation.id)
        list_active_events, err = EventsService.get_active_events_by_organisation_id(organisation.id)
        if err:
            return json.dumps(err)
        resp = make_response(
            render_template(
                'main/detail_organisation.html',
                organisation=organisation,
                list_employee=list_employee,
                count_employee=len(list_employee) if list_employee else 0,
                list_active_events=list_active_events,
                count_events=len(list_active_events) if list_active_events else 0,
            )
        )
        return resp

