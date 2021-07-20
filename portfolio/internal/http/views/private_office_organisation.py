import json

from flask import Blueprint, request, flash, make_response, url_for, render_template
from werkzeug.utils import redirect

from portfolio.internal.biz.deserializers.achievements import AchievementsDeserializer, DES_FOR_ADD_ACHIEVEMENT
from portfolio.internal.biz.deserializers.children_organisation import ChildrenOrganisationDeserializer
from portfolio.internal.biz.deserializers.employee import EmployeeDeserializer, DES_FOR_ADD_EMPLOYEE, \
    DES_FOR_EDIT_EMPLOYEE
from portfolio.internal.biz.deserializers.events import EventsDeserializer, DES_FOR_ADD_EVENT, DES_FOR_EDIT_EVENT
from portfolio.internal.biz.services.achievements import AchievementsService
from portfolio.internal.biz.services.achievements_child import AchievementsChildService
from portfolio.internal.biz.services.children_organisation import ChildrenOrganisationService
from portfolio.internal.biz.services.employee import EmployeeService
from portfolio.internal.biz.services.events import EventsService
from portfolio.internal.biz.services.events_child import EventsChildService
from portfolio.internal.biz.services.organisation import OrganisationService
from portfolio.internal.biz.services.request_to_organisation import RequestToOrganisationService
from portfolio.internal.biz.validators.achievements import AddAchievementSchema
from portfolio.internal.biz.validators.children import AddChildrenSchema
from portfolio.internal.biz.validators.employee import AddEmployeeSchema, EditEmployeeSchema
from portfolio.internal.biz.validators.events import AddEventSchema, EditEventSchema
from portfolio.internal.http.wrappers.organisation import get_org_id_and_acc_id_with_confirmed_email
from portfolio.models.account_main import AccountMain
from portfolio.models.achievements import Achievements
from portfolio.models.achievements_child import AchievementsChild
from portfolio.models.children_organisation import ChildrenOrganisation
from portfolio.models.employee import Employee
from portfolio.models.events import Events
from portfolio.models.events_child import EventsChild
from portfolio.models.organisation import Organisation
from portfolio.models.request_to_organisation import RequestToOrganisation

private_office_organisation = Blueprint('organisation/private_office', __name__, template_folder='templates/organisation/private_office', static_folder='static/organisation/private_office')


@private_office_organisation.route('/', methods=['GET'])
@get_org_id_and_acc_id_with_confirmed_email
def main_page(auth_account_main_id: int, organisation_id: int):
    if request.method == 'GET':
        organisation = Organisation(id=organisation_id)

        info_organisation, err = OrganisationService.get_by_id(organisation.id)
        if err:
            return json.dumps(err)

        list_employee, err = EmployeeService.get_list_employee_by_org_id(organisation.id)
        if err:
            return json.dumps(err)
        response = make_response(render_template(
            'organisation/index.html',
            info_organisation=info_organisation,
            list_employee=list_employee
        ))
        return response


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
        flash('Сотрудник успешно добавлен!')
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
        flash('Сотрудник успешно обновлен!')
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


@private_office_organisation.route('/detail_employee/<int:employee_id>', methods=['GET', 'POST'])
@get_org_id_and_acc_id_with_confirmed_email
def get_detail_employee(auth_account_main_id: int, organisation_id: int, employee_id: int):
    if request.method == "GET":
        organisation = Organisation(id=organisation_id)

        info_organisation, err = OrganisationService.get_by_id(organisation.id)
        if err:
            return json.dumps(err)

        employee = Employee(id=employee_id)
        employee, err = EmployeeService.get_by_employee_id(employee)
        if err:
            return json.dumps(err)
        response = make_response(
            render_template(
                'organisation/detail_teacher.html',
                employee=employee
            )
        )
        return response


@private_office_organisation.route('/add_event', methods=['POST', 'GET'])
@get_org_id_and_acc_id_with_confirmed_email
def add_event(auth_account_main_id: int, organisation_id: int):
    if request.method == 'POST':
        errors = AddEventSchema().validate(dict(type=request.form['type'],
                                                name=request.form['name'],
                                                date_event=request.form['date_event'],
                                                event_hours=request.form['hours'],
                                                skill=request.form['skill']))
        if errors:
            return json.dumps(errors)
        event: Events = EventsDeserializer.deserialize(request.form, DES_FOR_ADD_EVENT)
        event.organisation = Organisation(id=organisation_id)
        event, err = EventsService.add_event(event)
        if err:
            return None, err
        flash('Событие успешно добавлено')
        resp = make_response(
            redirect(url_for('organisation/private_office.get_list_events'))
        )
        return resp


@private_office_organisation.route('/requests', methods=['POST', 'GET'])
@get_org_id_and_acc_id_with_confirmed_email
def get_requests(auth_account_main_id: int, organisation_id: int):
    if request.method == 'GET':
        request_to_organisation = RequestToOrganisation(
            events=Events(
                organisation=Organisation(
                    id=organisation_id
                )
            )
        )
        list_request_to_organisation, err = RequestToOrganisationService.get_all_requests_by_org_id(request_to_organisation)
        if err:
            return json.dumps(err)
        resp = make_response(
            render_template(
                'organisation/requests.html',
                list_request=list_request_to_organisation
            )
        )
        return resp


@private_office_organisation.route('/requests/<int:request_id>', methods=['POST', 'GET'])
@get_org_id_and_acc_id_with_confirmed_email
def get_detail_request(auth_account_main_id: int, organisation_id: int, request_id: int):
    if request.method == 'GET':
        request_to_organisation = RequestToOrganisation(
            id=request_id,
            events=Events(organisation=Organisation(
                id=organisation_id)
            )
        )
        request_to_organisation, err = RequestToOrganisationService.get_request_by_org_id(request_to_organisation)
        if err:
            return json.dumps(err)
        resp = make_response(
            render_template(
                'organisation/detail_request.html',
                request_to_organisation=request_to_organisation
            )
        )
        return resp


@private_office_organisation.route('/requests/<int:request_id>/reject', methods=['POST', 'GET'])
@get_org_id_and_acc_id_with_confirmed_email
def reject_request(auth_account_main_id: int, organisation_id: int, request_id: int):
    if request.method == 'POST':
        request_to_organisation = RequestToOrganisation(
            id=request_id,
            events=Events(
                organisation=Organisation(
                    id=organisation_id
                )
            )
        )
        request_to_organisation, err = RequestToOrganisationService.delete_request(request_to_organisation)
        if err:
            return json.dumps(err)
        flash('Отклонено')
        resp = make_response(
            redirect(url_for('organisation/private_office.get_requests'))
        )
        return resp


@private_office_organisation.route('/requests/<int:request_id>/approve', methods=['POST', 'GET'])
@get_org_id_and_acc_id_with_confirmed_email
def approve_req(auth_account_main_id: int, organisation_id: int, request_id: int):
    if request.method == 'POST':
        request_to_organisation = RequestToOrganisation(
            id=request_id,
            events=Events(
                organisation=Organisation(
                    id=organisation_id,
                )
            )
        )
        request_to_organisation, err = RequestToOrganisationService.accept_request(request_to_organisation)
        if err:
            flash(err)
        resp = make_response(
            redirect(url_for('organisation/private_office.get_requests'))
        )
        return resp


@private_office_organisation.route('/learners', methods=['GET'])
@get_org_id_and_acc_id_with_confirmed_email
def get_list_learners(auth_account_main_id: int, organisation_id: int):
    if request.method == 'GET':
        list_learners, err = ChildrenOrganisationService.get_list_children_by_org_id(organisation_id)
        print(list_learners)
        if err:
            return json.dumps(err)
        resp = make_response(
            render_template(
                'organisation/pupils.html',
                list_learners=list_learners,
                count_learners=len(list_learners) if list_learners else 0,
            )
        )
        return resp


@private_office_organisation.route('/learners/<int:children_org_id>', methods=['GET'])
@get_org_id_and_acc_id_with_confirmed_email
def get_detail_children(children_org_id: int, auth_account_main_id: int, organisation_id: int):
    if request.method == 'GET':
        children_organisation = ChildrenOrganisation(id=children_org_id)
        activity_child, err = EventsChildService.get_by_children_organisation_id(children_organisation)
        if err:
            return json.dumps(err)
        children_org, err = ChildrenOrganisationService.get_children_by_children_org_id(children_organisation)
        if err:
            return json.dumps(err)
        list_achievements_for_completed_events, err = AchievementsService.get_all_by_completed_events_id(activity_child.list_completed_events)
        if err:
            return json.dumps(err)
        resp = make_response(
            render_template(
                'organisation/learner.html',
                count_complete_events=len(activity_child.list_completed_events) if activity_child.list_completed_events else 0,
                count_active_events=len(activity_child.list_active_events) if activity_child.list_active_events else 0,
                sum_hours=sum([completed_event.events.hours for completed_event in activity_child.list_completed_events]) if activity_child.list_completed_events else 0,
                activity_child=activity_child,
                list_achievements_for_completed_events=list_achievements_for_completed_events,
                children_org=children_org
            )
        )
        return resp


@private_office_organisation.route('/learners/<int:children_org_id>/<int:events_id>/update_status', methods=['POST'])
@get_org_id_and_acc_id_with_confirmed_email
def update_status_event_for_child(children_org_id: int, auth_account_main_id: int, organisation_id: int, events_id: int):
    if request.method == 'POST':
        events_child = EventsChild(
            events=Events(id=events_id),
            children_organisation=ChildrenOrganisation(id=children_org_id),
            status=request.form.get('status_event')
        )
        events_child, err = EventsChildService.update_status(events_child)
        if err:
            return None, err
        flash("Успешно обновлено!")
        resp = make_response(
            redirect(url_for('organisation/private_office.get_detail_children', children_org_id=children_org_id))
        )
        return resp


@private_office_organisation.route('/learners/<int:children_org_id>/<int:events_id>/update_complete_event', methods=['POST'])
@get_org_id_and_acc_id_with_confirmed_email
def update_complete_event_for_child(children_org_id: int, auth_account_main_id: int, organisation_id: int, events_id: int):
    if request.method == "POST":
        count_hours = request.form.get('hours')
        events_child = EventsChild(children_organisation=ChildrenOrganisation(id=children_org_id),
                                   events=Events(id=events_id,
                                                 hours=count_hours))
        events_child, err = EventsChildService.update_hours(events_child)
        if err:
            return None, err
        flash('Успешно обнолено!')
        resp = make_response(
            redirect(url_for('organisation/private_office.get_detail_children', children_org_id=children_org_id))
        )
        return resp


@private_office_organisation.route('/learners/<int:children_org_id>/add_achievement_for_child', methods=['POST'])
@get_org_id_and_acc_id_with_confirmed_email
def add_achievement_for_child(children_org_id: int, auth_account_main_id: int, organisation_id: int):
    if request.method == 'POST':
        print(request.headers.get("Referer"))
        achievements_child = AchievementsChild(
            point=request.form.get('point'),
            achievements=Achievements(id=request.form.get('achievement_id')),
            children_organisation=ChildrenOrganisation(id=children_org_id)
        )
        achievements_child, err = AchievementsChildService.add_achievement(achievements_child)
        if err:
            return json.dumps(err)
        resp = make_response(
            redirect(url_for('organisation/private_office.get_detail_children', children_org_id=children_org_id))
        )
        return resp


@private_office_organisation.route('/learners/<int:children_org_id>/<int:achievement_child_id>/update_achievement_for_child', methods=['POST'])
@get_org_id_and_acc_id_with_confirmed_email
def update_achievement_child(children_org_id: int, auth_account_main_id: int, organisation_id: int, achievement_child_id:int):
    if request.method == 'POST':
        achievement_child = AchievementsChild(
            id=achievement_child_id,
            achievements=Achievements(id=request.form.get('achievement_id')),
            point=request.form.get('point')
        )
        achievement_child, err = AchievementsChildService.update_by_id(achievement_child)
        if err:
            return None, err
        resp = make_response(
            redirect(url_for('organisation/private_office.get_detail_children', children_org_id=children_org_id))
        )
        return resp


@private_office_organisation.route('/learners/<int:children_org_id>/<int:achievement_child_id>/delete_achievement_for_child', methods=['POST'])
@get_org_id_and_acc_id_with_confirmed_email
def delete_achievement_for_child(children_org_id: int, auth_account_main_id: int, organisation_id: int, achievement_child_id:int):
    if request.method == 'POST':
        achievement_child = AchievementsChild(
            id=achievement_child_id,
            achievements=Achievements(id=request.form.get('achievement_id')),
            point=request.form.get('point')
        )
        achievement_child, err = AchievementsChildService.delete_by_id(achievement_child)
        if err:
            return None, err

        resp = make_response(
            redirect(url_for('organisation/private_office.get_detail_children', children_org_id=children_org_id))
        )
        return resp


@private_office_organisation.route('/events', methods=['GET'])
@get_org_id_and_acc_id_with_confirmed_email
def get_list_events(auth_account_main_id: int, organisation_id: int):
    if request.method == 'GET':
        list_events, err = EventsService.get_all_events_by_organisation_id(organisation_id)
        if err:
            return json.dumps(err)
        response = make_response(
            render_template(
                'organisation/events.html',
                list_events=list_events
            )
        )
        return response


@private_office_organisation.route('events/<int:events_id>', methods=['GET'])
@get_org_id_and_acc_id_with_confirmed_email
def detail_event(auth_account_main_id: int, organisation_id: int, events_id: int):
    if request.method == 'GET':
        events = Events(id=events_id)
        event, err = EventsService.get_by_events_id(events)
        if err:
            return json.dumps(err)

        achievements = Achievements(events=event)
        list_achievements, err = AchievementsService.get_by_events_id(achievements)
        if err:
            return json.dumps(err)

        resp = make_response(
            render_template(
                'organisation/detail_event.html',
                event=event,
                list_achievements=list_achievements
            ),
        )
        return resp


@private_office_organisation.route('events/<int:events_id>/edit_event', methods=["POST"])
@get_org_id_and_acc_id_with_confirmed_email
def edit_event(auth_account_main_id: int, organisation_id: int, events_id: int):
    if request.method == 'POST':
        errors = EditEventSchema().validate(dict(type=request.form.get('type'),
                                                 name=request.form.get('name'),
                                                 date_event=request.form.get('date_event'),
                                                 hours=request.form.get('event_hours'),
                                                 skill=request.form.get('skill')))
        if errors:
            return json.dumps(errors)
        print(request.form)
        event = EventsDeserializer.deserialize(request.form, DES_FOR_EDIT_EVENT)
        event.id = events_id
        event, err = EventsService.update_event(event)
        if err:
            return json.dumps(err)
        flash('Успешно обнолено!')
        resp = make_response(
            redirect(url_for('organisation/private_office.detail_event', events_id=events_id))
        )
        return resp


@private_office_organisation.route('events/<int:events_id>/add_achievement', methods=['GET', 'POST'])
@get_org_id_and_acc_id_with_confirmed_email
def add_achievement(auth_account_main_id: int, organisation_id: int, events_id: int):
    if request.method == 'POST':
        errors = AddAchievementSchema().validate(dict(name=request.form['name'],
                                                      nomination=request.form['nomination'],
                                                      points=request.form['points']))
        if errors:
            return json.dumps(errors)
        achievement = AchievementsDeserializer.deserialize(request.form, DES_FOR_ADD_ACHIEVEMENT)
        achievement.events = Events(id=events_id)
        achievement, err = AchievementsService.add_achievement(achievement)
        if err:
            return flash(err)
        flash('Успешно добавили достижение!')
        resp = make_response(
            redirect(url_for('organisation/private_office.detail_event', events_id=events_id))
        )
        return resp


@private_office_organisation.route('events/<int:events_id>/delete_achievement/<int:achievement_id>', methods=['GET', 'POST'])
@get_org_id_and_acc_id_with_confirmed_email
def delete_achievement(auth_account_main_id: int, organisation_id: int, events_id: int, achievement_id: int):
    if request.method == 'POST':
        achievement = Achievements(
            id=achievement_id,
            events=Events(id=events_id)
        )
        achievement, err = AchievementsService.delete_achievement(achievement)
        if err:
            return flash(err)
        flash('Успешно удалено')
        resp = make_response(
            redirect(url_for('organisation/private_office.detail_event', events_id=events_id))
        )
        return resp
