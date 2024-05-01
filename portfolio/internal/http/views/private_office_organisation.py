import json
from datetime import date, datetime

from flask import Blueprint, request, flash, make_response, url_for, render_template
from werkzeug.utils import redirect

from enums.success.success_enum import SuccessEnum
from internal.biz.deserializers.achievements import AchievementsDeserializer, DES_FOR_ADD_ACHIEVEMENT, \
    DES_FOR_EDIT_ACHIEVEMENT
from internal.biz.deserializers.employee import EmployeeDeserializer, DES_FOR_ADD_EMPLOYEE, \
    DES_FOR_EDIT_EMPLOYEE
from internal.biz.deserializers.events import EventsDeserializer, DES_FOR_ADD_EVENT, DES_FOR_EDIT_EVENT
from internal.biz.services.achievements import AchievementsService
from internal.biz.services.achievements_child import AchievementsChildService
from internal.biz.services.children_organisation import ChildrenOrganisationService
from internal.biz.services.employee import EmployeeService
from internal.biz.services.events import EventsService
from internal.biz.services.events_child import EventsChildService
from internal.biz.services.organisation import OrganisationService
from internal.biz.services.request_to_organisation import RequestToOrganisationService
from internal.biz.services.utils import calculate_age
from internal.biz.validators.achievements import AddAchievementSchema, EditAchievementSchema
from internal.biz.validators.children import AddChildrenSchema
from internal.biz.validators.employee import AddEmployeeSchema, EditEmployeeSchema
from internal.biz.validators.events import AddEventSchema, EditEventSchema
from internal.biz.validators.utils import get_calendar
from internal.http.wrappers.organisation import get_org_id_and_acc_id_with_confirmed_email
from models.account_main import AccountMain
from models.achievements import Achievements
from models.achievements_child import AchievementsChild
from models.children_organisation import ChildrenOrganisation
from models.employee import Employee
from models.events import Events
from models.events_child import EventsChild
from models.organisation import Organisation
from models.request_to_organisation import RequestToOrganisation

private_office_organisation = Blueprint('organisation/private_office', __name__, template_folder='templates/organisation/private_office', static_folder='static/organisation/private_office')


@private_office_organisation.route('/', methods=['GET'])
@get_org_id_and_acc_id_with_confirmed_email
def main_page(auth_account_main_id: int, organisation_id: int):
    if request.method == 'GET':
        organisation = Organisation(id=organisation_id)

        info_organisation, err = OrganisationService.get_by_id(organisation.id)
        if err:
            flash(err)
            return make_response(
                redirect(request.headers.get("Referer"))
            )

        list_employee, err = EmployeeService.get_list_employee_by_org_id(organisation.id)
        if err:
            flash(err)
            return make_response(
                redirect(request.headers.get("Referer"))
            )
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
            flash(str(errors))
            return make_response(
                redirect(request.headers.get("Referer"))
            )
        teacher = EmployeeDeserializer.deserialize(request.form, DES_FOR_ADD_EMPLOYEE)
        teacher.organisation = Organisation(id=organisation_id,
                                            account_main=AccountMain(id=auth_account_main_id))
        teacher, err = EmployeeService.add_employee(teacher)
        if err:
            flash(err)
            return make_response(
                redirect(request.headers.get("Referer"))
            )

        flash(SuccessEnum.add)
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
            flash(str(errors))
            return make_response(
                redirect(request.headers.get("Referer"))
            )

        employee = EmployeeDeserializer.deserialize(request.form, DES_FOR_EDIT_EMPLOYEE)
        employee.id = employee_id
        teacher, err = EmployeeService.update_employee(employee)
        if err:
            flash(err)
            return make_response(
                redirect(request.headers.get("Referer"))
            )

        flash(SuccessEnum.update)
        response = make_response(
            redirect(
                url_for(
                    'organisation/private_office.get_detail_employee',
                    employee_id=employee_id
                )
            )
        )
        return response


@private_office_organisation.route('/delete_employee/<int:employee_id>', methods=['POST'])
@get_org_id_and_acc_id_with_confirmed_email
def delete_employee(auth_account_main_id: int, organisation_id: int, employee_id: int):
    if request.method == "POST":
        employee = Employee(id=employee_id)
        employee, err = EmployeeService.delete_employee(employee)
        if err:
            flash(err)
            return make_response(
                redirect(request.headers.get("Referer"))
            )

        flash(SuccessEnum.delete)
        resp = make_response(
            redirect(
                url_for(
                    'organisation/private_office.main_page'
                )
            )
        )
        return resp


@private_office_organisation.route('/detail_employee/<int:employee_id>', methods=['GET', 'POST'])
@get_org_id_and_acc_id_with_confirmed_email
def get_detail_employee(auth_account_main_id: int, organisation_id: int, employee_id: int):
    if request.method == "GET":
        organisation = Organisation(id=organisation_id)

        info_organisation, err = OrganisationService.get_by_id(organisation.id)
        if err:
            flash(err)
            return make_response(
                redirect(request.headers.get("Referer"))
            )

        employee = Employee(id=employee_id)
        employee, err = EmployeeService.get_by_employee_id(employee)
        if err:
            flash(err)
            return make_response(
                redirect(request.headers.get("Referer"))
            )

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
            flash(str(errors))
            return make_response(
                redirect(request.headers.get("Referer"))
            )

        event: Events = EventsDeserializer.deserialize(request.form, DES_FOR_ADD_EVENT)
        event.organisation = Organisation(id=organisation_id)
        event, err = EventsService.add_event(event)
        if err:
            flash(err)
            return make_response(
                redirect(request.headers.get("Referer"))
            )

        flash(SuccessEnum.add)
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
            flash(err)
            return make_response(
                redirect(request.headers.get("Referer"))
            )

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
            flash(err)
            return make_response(
                redirect(request.headers.get("Referer"))
            )

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
            flash(err)
            return make_response(
                redirect(request.headers.get("Referer"))
            )

        flash(SuccessEnum.reject)
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
            return make_response(
                redirect(request.headers.get("Referer"))
            )

        resp = make_response(
            redirect(url_for('organisation/private_office.get_requests'))
        )
        return resp


@private_office_organisation.route('/learners', methods=['GET'])
@get_org_id_and_acc_id_with_confirmed_email
def get_list_learners(auth_account_main_id: int, organisation_id: int):
    if request.method == 'GET':
        list_learners, err = ChildrenOrganisationService.get_list_children_by_org_id(organisation_id)
        if err:
            flash(err)
            return make_response(
                redirect(request.headers.get("Referer"))
            )

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
            flash(err)
            return make_response(
                redirect(request.headers.get("Referer"))
            )

        children_org, err = ChildrenOrganisationService.get_children_by_children_org_id(children_organisation)
        if err:
            flash(err)
            return make_response(
                redirect(request.headers.get("Referer"))
            )

        list_achievements_for_completed_events, err = AchievementsService.get_all_by_completed_events_id(activity_child.list_completed_events)
        if err:
            flash(err)
            return make_response(
                redirect(request.headers.get("Referer"))
            )

        resp = make_response(
            render_template(
                'organisation/learner.html',
                count_complete_events=len(activity_child.list_completed_events) if activity_child.list_completed_events else 0,
                count_active_events=len(activity_child.list_active_events) if activity_child.list_active_events else 0,
                sum_hours=sum([completed_event.events.hours for completed_event in activity_child.list_completed_events]) if activity_child.list_completed_events else 0,
                activity_child=activity_child,
                list_achievements_for_completed_events=list_achievements_for_completed_events,
                children_org=children_org,
                age=calculate_age(children_org.children.date_born)
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
            status=True if request.form.get('status_event') == 'True' else False
        )
        events_child, err = EventsChildService.update_status(events_child)
        if err:
            flash(err)
            return make_response(
                redirect(request.headers.get("Referer"))
            )

        flash(SuccessEnum.update)
        resp = make_response(
            redirect(url_for('organisation/private_office.get_detail_children', children_org_id=children_org_id))
        )
        return resp


@private_office_organisation.route('/learners/<int:children_org_id>/<int:events_id>/update_complete_event', methods=['POST'])
@get_org_id_and_acc_id_with_confirmed_email
def update_complete_event_for_child(children_org_id: int, auth_account_main_id: int, organisation_id: int, events_id: int):
    if request.method == "POST":
        count_hours = request.form.get('hours')
        events_child = EventsChild(
            hours_event=count_hours,
            children_organisation=ChildrenOrganisation(
                id=children_org_id),
            events=Events(
                id=events_id,
            )
        )
        events_child, err = EventsChildService.update_hours(events_child)
        if err:
            flash(err)
            return make_response(
                redirect(request.headers.get("Referer"))
            )

        flash(SuccessEnum.update)
        resp = make_response(
            redirect(url_for('organisation/private_office.get_detail_children', children_org_id=children_org_id))
        )
        return resp


@private_office_organisation.route('/learners/<int:children_org_id>/add_achievement_for_child', methods=['POST'])
@get_org_id_and_acc_id_with_confirmed_email
def add_achievement_for_child(children_org_id: int, auth_account_main_id: int, organisation_id: int):
    if request.method == 'POST':
        achievements_child = AchievementsChild(
            point=request.form.get('point'),
            achievements=Achievements(id=request.form.get('achievement_id')),
            children_organisation=ChildrenOrganisation(id=children_org_id)
        )
        achievements_child, err = AchievementsChildService.add_achievement(achievements_child)
        if err:
            flash(err)
            return make_response(
                redirect(request.headers.get("Referer"))
            )

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
            flash(err)
            return make_response(
                redirect(request.headers.get("Referer"))
            )

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
            flash(err)
            return make_response(
                redirect(request.headers.get("Referer"))
            )

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
            flash(err)
            return make_response(
                redirect(request.headers.get("Referer"))
            )

        response = make_response(
            render_template(
                'organisation/events.html',
                list_events=list_events
            )
        )
        return response


@private_office_organisation.route('/events/<int:events_id>', methods=['GET'])
@get_org_id_and_acc_id_with_confirmed_email
def detail_event(auth_account_main_id: int, organisation_id: int, events_id: int):
    if request.method == 'GET':
        events = Events(id=events_id)
        event, err = EventsService.get_by_events_id(events)
        if err:
            flash(err)
            return make_response(
                redirect(request.headers.get("Referer"))
            )

        achievements = Achievements(events=event)
        list_achievements, err = AchievementsService.get_by_events_id(achievements)
        if err:
            flash(err)
            return make_response(
                redirect(request.headers.get("Referer"))
            )

        resp = make_response(
            render_template(
                'organisation/detail_event.html',
                event=event,
                list_achievements=list_achievements
            ),
        )
        return resp


@private_office_organisation.route('/events/<int:events_id>/edit_event', methods=["POST"])
@get_org_id_and_acc_id_with_confirmed_email
def edit_event(auth_account_main_id: int, organisation_id: int, events_id: int):
    if request.method == 'POST':
        errors = EditEventSchema().validate(dict(type=request.form.get('type'),
                                                 name=request.form.get('name'),
                                                 date_event=request.form.get('date_event'),
                                                 hours=request.form.get('event_hours'),
                                                 skill=request.form.get('skill')))
        if errors:
            flash(str(errors))
            return make_response(
                redirect(request.headers.get("Referer"))
            )

        event = EventsDeserializer.deserialize(request.form, DES_FOR_EDIT_EVENT)
        event.id = events_id
        event, err = EventsService.update_event(event)
        if err:
            flash(err)
            return make_response(
                redirect(request.headers.get("Referer"))
            )

        flash(SuccessEnum.update)
        resp = make_response(
            redirect(url_for('organisation/private_office.detail_event', events_id=events_id))
        )
        return resp


@private_office_organisation.route('/events/<int:events_id>/add_achievement', methods=['GET', 'POST'])
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
            flash(err)
            return make_response(
                redirect(request.headers.get("Referer"))
            )

        flash(SuccessEnum.add)
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
            flash(err)
            return make_response(
                redirect(request.headers.get("Referer"))
            )

        flash(SuccessEnum.delete)
        resp = make_response(
            redirect(url_for('organisation/private_office.detail_event', events_id=events_id))
        )
        return resp


@private_office_organisation.route('events/<int:events_id>/edit_achievement/<int:achievement_id>', methods=['GET', 'POST'])
@get_org_id_and_acc_id_with_confirmed_email
def edit_achievement(auth_account_main_id: int, organisation_id: int, events_id: int, achievement_id: int):
    if request.method == 'POST':
        errors = EditAchievementSchema().validate(dict(name=request.form.get('name'),
                                                       nomination=request.form.get('nomination'),
                                                       points=request.form.get('points')))
        if errors:
            flash(str(errors))
            return make_response(
                redirect(request.headers.get("Referer"))
            )

        achievement = AchievementsDeserializer.deserialize(request.form, DES_FOR_EDIT_ACHIEVEMENT)
        achievement.id = achievement_id
        achievement.events = Events(id=events_id)
        achievement, err = AchievementsService.edit_achievement(achievement)
        if err:
            flash(err)
            return make_response(
                redirect(request.headers.get("Referer"))
            )

        flash(SuccessEnum.update)
        resp = make_response(
            redirect(url_for('organisation/private_office.detail_event', events_id=events_id))
        )
        return resp


@private_office_organisation.route('/calendar', methods=['GET', 'POST'])
@get_org_id_and_acc_id_with_confirmed_email
def calendar(auth_account_main_id: int, organisation_id: int):
    if request.method == 'GET':
        calendar_date = request.args.get('calendar_date')
        if not calendar_date:
            calendar_date = date.today()
        else:
            calendar_date = datetime.strptime(calendar_date, '%Y-%m-%d').date()

        events_for_date, err = EventsService.get_events_by_date(organisation_id, calendar_date)
        if err:
            flash(err)
            return make_response(
                redirect(request.headers.get("Referer"))
            )

        calendar, month_str = get_calendar()
        resp = make_response(
            render_template(
                'organisation/calendar.html',
                events_for_date=events_for_date,
                calendar=calendar,
                month_str=month_str,
                calendar_date=calendar_date
            )
        )
        return resp
