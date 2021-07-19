from datetime import datetime, date

from flask import Blueprint, request, json, make_response, render_template, url_for, flash
from werkzeug.utils import redirect

from portfolio.models.account_main import AccountMain
from portfolio.models.children import Children
from portfolio.models.parents import Parents

private_office_parents = Blueprint('parents/private_office', __name__, template_folder='templates/private_office', static_folder='static/private_office')


@private_office_parents.route('/main', methods=['GET', 'POST'])
@check_account_role_parents_and_login_required
def index(auth_account_main_id: int):
    if request.method == 'GET':
        children = Children(parents=Parents(account_main=AccountMain(id=auth_account_main_id)))

        list_children, err = ChildrenService.get_children_by_parents_id(children)
        if err:
            return json.dumps(err)
        tuple_children_id = tuple([child.id for child in list_children])
        context = []
        for child in list_children:
            events_child = EventsChild(children_organisation=ChildrenOrganisation(children=Children(id=child.id)))
            list_events, err = EventsChildService.get_completed_events_by_child_id(events_child)
            if err:
                return json.dumps(err)
            context.append({
                "children_info": child,
                "events_info": list_events
            })

        response = make_response(render_template(
            'parents/index.html',
            context=context
        ))
        return response


@private_office_parents.route('/progress/<children_id>', methods=['GET'])
@check_account_role_parents_and_login_required
def progress(children_id: int, auth_account_main_id: int):
    if request.method == 'GET':
        if children_id == 'A':
            children = Children(parents=Parents(account_main=AccountMain(id=auth_account_main_id)))
            list_children, err = ChildrenService.get_children_by_parents_id(children)
            if err:
                return json.dumps(err)
            resp = make_response(
                render_template(
                    'parents/progress_for_all.html',
                    list_children=list_children
                )
            )
            return resp
        else:
            children = Children(id=children_id, parents=Parents(account_main=AccountMain(id=auth_account_main_id)))
            children, err = ChildrenService.get_by_id(children)

            events_child = EventsChild(children_organisation=ChildrenOrganisation(children=children))
            active_events, err = EventsChildService.get_active_events_by_child_id(events_child)
            if err:
                return json.dumps(err)
            list_completed_events, err = EventsChildService.get_completed_events_by_child_id(events_child)

            if err:
                return json.dumps(err)

            children_organisation = ChildrenOrganisation(children=children)
            list_organisation_for_child, err = ChildrenOrganisationService.get_list_organisation_by_children_id(children_organisation)
            if err:
                return json.dumps(err)

            gap_for_skill = request.args.get('gap_for_skill')
            if not gap_for_skill:
                gap_for_skill = date.min
            dict_by_unique_skill, err = EventsChildService.get_statistic_by_skill(events_child, gap_for_skill)
            if err:
                return json.dumps(err)

            gap_for_org = request.args.get('gap_for_org')
            if not gap_for_org:
                gap_for_org = date.min

            dict_by_unique_organisation, err = EventsChildService.get_statistic_by_org(events_child, gap_for_org)
            if err:
                return json.dumps(err)

            max_focus_event, err = EventsChildService.get_statistic_focus_time(events_child)
            if err:
                return json.dumps(err)

            achievements_child = AchievementsChild(children_organisation=children_organisation)
            list_achievements_child, err = AchievementsChildService.get_all_achievements_by_child_id(achievements_child)
            if err:
                return json.dumps(err)

            resp = make_response(render_template(
                'parents/progress.html',
                children=children,
                active_events=active_events,
                count_active_events=len(active_events) if active_events else 0,
                count_completed_events=len(list_completed_events) if list_completed_events else 0,
                all_hours=sum(complete_event.events.hours for complete_event in list_completed_events) if list_completed_events else 0,
                list_completed_events=list_completed_events,
                list_org=list_organisation_for_child,
                dict_by_unique_skill=dict_by_unique_skill,
                dict_by_unique_organisation=dict_by_unique_organisation,
                max_focus_event=max_focus_event,
                list_achievements_child=list_achievements_child,
                gap_for_org=gap_for_org,
                gap_for_skill=gap_for_skill,
            ))
            return resp


@private_office_parents.route('/progress/<int:children_id>/edit_children', methods=['POST'])
@check_account_role_parents_and_login_required
def edit_children(auth_account_main_id: int, children_id: int):
    if request.method == 'POST':
        errors = EddChildSchema().validate(dict(name=request.form['name'],
                                                surname=request.form['surname'],
                                                date_born=request.form['date_born']))
        if errors:
            return json.dumps(errors)

        children = ChildrenDeserialize.deserialize(request.form, DES_FOR_EDIT_CHILD)
        children.id = children_id
        children.parents = Parents(account_main=AccountMain(id=auth_account_main_id))

        children, err = ChildrenService.edit_child(children)
        if err:
            return json.dumps(err)
        flash('Успешно обновлено!')
        resp = make_response(
            redirect(
                url_for('parents/private_office.progress', children_id=children_id)
            )
        )
        return resp


@private_office_parents.route('/', methods=['GET', 'POST', 'PATCH', 'DELETE'])
@check_account_role_parents_and_login_required
def main(auth_account_main_id: int):
    if request.method == 'GET':
        children = Children(parents=Parents(account_main=AccountMain(id=auth_account_main_id)))

        list_children, err = ChildrenService.get_children_by_parents_id(children)
        if err:
            return json.dumps(err)

        return json.dumps(get_response_get_list_child(list_children))

    elif request.method == 'POST':
        errors = AddChildSchema().validate(dict(name=request.form['name'],
                                                surname=request.form['surname'],
                                                date_born=request.form['date_born']))
        if errors:
            return json.dumps(errors)

        children = ChildrenDeserialize.deserialize(request.form, DES_FOR_ADD_CHILD)
        children.parents = Parents(account_main=AccountMain(id=auth_account_main_id))

        children, err = ChildrenService.add_child(children)
        if err:
            return json.dumps(err)

        response = make_response(redirect(url_for("parents/private_office.index")))
        flash("Успешно добавлен")
        return response
    elif request.method == 'DELETE':
        children = Children(parents=Parents(account_main=AccountMain(id=auth_account_main_id)))

        children, err = ChildrenService.delete_child(children)
        if err:
            return json.dumps(err)

        return json.dumps(get_response_delete_children(children))
    else:
        raise NotImplementedError


@private_office_parents.route('/children/<int:children_id>', methods=['GET', 'POST'])
# @check_account_role_parents
@required_auth_with_confirmed_email
@get_sort_statistic
@get_sort_focus
@get_query_params_search_event
def detail_child(result_sort_statistic: datetime.date, result_sort_focus: datetime.date, auth_account_main_id: int, children_id: int, events_id: int):
    if request.method == 'GET':
        events_child = EventsChild(
            children_organisation=ChildrenOrganisation(
                children=Children(
                    id=children_id
                )
            )
        )
        activity_child, err = EventsChildService.get_by_children_id(events_child)
        if err:
            return json.dumps(err)

        statistic_dict, err = StatisticService.get_result_statistic(result_sort_statistic, children_id)
        if err:
            return None, err

        focus_dict, err = StatisticService.get_result_focus(result_sort_focus, children_id)
        if err:
            return None, err

        return json.dumps(get_response_detail_activity_children(activity_child))
    elif request.method == 'POST':
        if not events_id:
            return json.dumps('Выберите событие')
        request_to_organisation = RequestToOrganisation(
            children=Children(id=children_id),
            parents=Parents(account_main=AccountMain(id=auth_account_main_id)),
            events=Events(id=events_id))

        request_to_organisation, err = RequestToOrganisationService.make_request_up(request_to_organisation)
        if err:
            return json.dumps(err)
        return json.dumps(get_response_make_request(request_to_organisation))
    else:
        raise NotImplementedError
