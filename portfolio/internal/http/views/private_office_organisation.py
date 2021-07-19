import json

from flask import Blueprint, request, flash, make_response, url_for
from werkzeug.utils import redirect

from portfolio.internal.biz.deserializers.employee import EmployeeDeserializer, DES_FOR_ADD_EMPLOYEE, \
    DES_FOR_EDIT_EMPLOYEE
from portfolio.internal.biz.services.employee import EmployeeService
from portfolio.internal.biz.validators.employee import AddEmployeeSchema, EditEmployeeSchema
from portfolio.internal.http.wrappers.organisation import get_org_id_and_acc_id_with_confirmed_email
from portfolio.models.account_main import AccountMain
from portfolio.models.employee import Employee
from portfolio.models.organisation import Organisation

private_office_organisation = Blueprint('organisation/private_office', __name__, template_folder='templates/organisation/private_office', static_folder='static/organisation/private_office')


@private_office_organisation.route('/add_employee', methods=['POST', 'GET'])
@get_org_id_and_acc_id_with_confirmed_email
def add_employee(auth_account_main_id: int, organisation_id: int):
    if request.method == 'POST':
        errors = AddEmployeeSchema().validate(dict(login=request.form['login'],
                                                   name=request.form['name'],
                                                   surname=request.form['surname'],
                                                   specialty=request.form['specialty']))
        if errors:
            return json.dumps(errors)
        teacher = EmployeeDeserializer.deserialize(request.form, DES_FOR_ADD_EMPLOYEE)
        teacher.organisation = Organisation(id=organisation_id,
                                            account_main=AccountMain(id=auth_account_main_id))
        teacher, err = EmployeeService.add_employee(teacher)
        if err:
            return json.dumps(err)
        flash('Учитель успешно добавлен!')
        response = make_response(
            redirect(url_for('organisation/private_office.main_page'))
        )
        return response


@private_office_organisation.route('/edit_employee/<int:employee_id>', methods=['POST'])
@get_org_id_and_acc_id_with_confirmed_email
def edit_employee(auth_account_main_id: int, organisation_id: int, employee_id: int):
    if request.method == "POST":
        errors = EditEmployeeSchema().validate(dict(login=request.form['login'],
                                                    name=request.form['name'],
                                                    surname=request.form['surname'],
                                                    specialty=request.form['specialty']))
        if errors:
            return json.dumps(errors)

        employee = EmployeeDeserializer.deserialize(request.form, DES_FOR_EDIT_EMPLOYEE)
        employee.id = employee_id
        teacher, err = EmployeeService.update_employee(employee)
        if err:
            return json.dumps(err)
        flash('Учитель успешно обновлен!')
        response = make_response(
            redirect(url_for('organisation/private_office.main_page'))
        )
        return response


@private_office_organisation.route('/delete_employee/<int:employee_id>', methods=['POST'])
@get_org_id_and_acc_id_with_confirmed_email
def delete_employee(auth_account_main_id: int, organisation_id: int, employee_id: int):
    if request.method == "POST":
        employee = Employee(id=employee_id)
        employee, err = EmployeeService.delete_employee(employee)
        if err:
            return json.dumps(err)
        flash("Успешно удален")
        resp = make_response(
            redirect(url_for(
                'organisation/private_office.main_page'
            ))
        )
        return resp
