from datetime import datetime, date

from flask import Blueprint, request, json, make_response, render_template, url_for, flash
from werkzeug.utils import redirect

from portfolio.enums.success.success_enum import SuccessEnum
from portfolio.internal.biz.deserializers.children import ChildrenDeserialize, DES_FOR_EDIT_CHILD, DES_FOR_ADD_CHILD
from portfolio.internal.biz.services.achievements_child import AchievementsChildService
from portfolio.internal.biz.services.children import ChildrenService
from portfolio.internal.biz.services.children_organisation import ChildrenOrganisationService
from portfolio.internal.biz.services.events_child import EventsChildService
from portfolio.internal.biz.validators.children import EditChildSchema, AddChildrenSchema
from portfolio.internal.biz.validators.utils import get_calendar
from portfolio.internal.http.wrappers.parents import get_parent_id_and_acc_id_with_confirmed_email
from portfolio.models.account_main import AccountMain
from portfolio.models.achievements_child import AchievementsChild
from portfolio.models.children import Children
from portfolio.models.children_organisation import ChildrenOrganisation
from portfolio.models.events_child import EventsChild
from portfolio.models.parents import Parents

private_office_parents = Blueprint('parents/private_office', __name__, template_folder='templates/private_office', static_folder='static/private_office')


@private_office_parents.route('/main', methods=['GET', 'POST'])
@get_parent_id_and_acc_id_with_confirmed_email
def index(auth_account_main_id: int, parent_id: int):
    if request.method == 'GET':
        children = Children(
            parents=Parents(
                id=parent_id,
                account_main=AccountMain(
                    id=auth_account_main_id)
            )
        )

        list_children, err = ChildrenService.get_children_by_parents_id(children)
        if err:
            flash(err)
            return make_response(
                redirect(request.headers.get("Referer"))
            )

        context = []
        if list_children:
            for child in list_children:
                events_child = EventsChild(children_organisation=ChildrenOrganisation(children=Children(id=child.id)))
                list_events, err = EventsChildService.get_completed_events_by_child_id(events_child)
                if err:
                    flash(err)
                    return make_response(
                        redirect(request.headers.get("Referer"))
                    )

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
@get_parent_id_and_acc_id_with_confirmed_email
def progress(children_id: int, auth_account_main_id: int, parent_id: int):
    if request.method == 'GET':
        if children_id == 'A':
            children = Children(
                parents=Parents(
                    id=parent_id,
                )
            )
            list_children, err = ChildrenService.get_children_by_parents_id(children)
            if err:
                flash(err)
                return make_response(
                    redirect(request.headers.get("Referer"))
                )

            resp = make_response(
                render_template(
                    'parents/progress_for_all.html',
                    list_children=list_children
                )
            )
            return resp
        else:
            children = Children(
                id=children_id
            )
            children, err = ChildrenService.get_by_id(children)
            children.parents = Parents(id=parent_id)

            events_child = EventsChild(children_organisation=ChildrenOrganisation(children=children))
            active_events, err = EventsChildService.get_active_events_by_child_id(events_child)
            if err:
                flash(err)
                return make_response(
                    redirect(request.headers.get("Referer"))
                )

            list_completed_events, err = EventsChildService.get_completed_events_by_child_id(events_child)

            if err:
                flash(err)
                return make_response(
                    redirect(request.headers.get("Referer"))
                )

            children_organisation = ChildrenOrganisation(children=children)
            list_organisation_for_child, err = ChildrenOrganisationService.get_list_organisation_by_children_id(children_organisation)
            if err:
                flash(err)
                return make_response(
                    redirect(request.headers.get("Referer"))
                )

            gap_for_skill = request.args.get('gap_for_skill')
            if not gap_for_skill:
                gap_for_skill = date.min
            dict_by_unique_skill, err = EventsChildService.get_statistic_by_skill(events_child, gap_for_skill)
            if err:
                flash(err)
                return make_response(
                    redirect(request.headers.get("Referer"))
                )

            gap_for_org = request.args.get('gap_for_org')
            if not gap_for_org:
                gap_for_org = date.min

            dict_by_unique_organisation, err = EventsChildService.get_statistic_by_org(events_child, gap_for_org)
            if err:
                flash(err)
                return make_response(
                    redirect(request.headers.get("Referer"))
                )

            max_focus_event, err = EventsChildService.get_statistic_focus_time(events_child)
            if err:
                flash(err)
                return make_response(
                    redirect(request.headers.get("Referer"))
                )

            achievements_child = AchievementsChild(children_organisation=children_organisation)
            list_achievements_child, err = AchievementsChildService.get_all_achievements_by_child_id(achievements_child)
            if err:
                flash(err)
                return make_response(
                    redirect(request.headers.get("Referer"))
                )

            calendar_date = request.args.get('calendar_date')
            if not calendar_date:
                calendar_date = date.today()
            else:
                calendar_date = datetime.strptime(calendar_date, '%Y-%m-%d').date()
            events_for_date, err = EventsChildService.get_events_by_date(children_id, calendar_date)
            if err:
                flash(err)
                return make_response(
                    redirect(request.headers.get("Referer"))
                )

            calendar, month_str = get_calendar()
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
                events_for_date=events_for_date,
                month_str=month_str,
                calendar=calendar,
                calendar_date=calendar_date
            ))
            return resp


@private_office_parents.route('/progress/<int:children_id>/edit_children', methods=['POST'])
@get_parent_id_and_acc_id_with_confirmed_email
def edit_children(auth_account_main_id: int, children_id: int, parent_id: int):
    if request.method == 'POST':
        errors = EditChildSchema().validate(dict(name=request.form['name'],
                                                 surname=request.form['surname'],
                                                 date_born=request.form['date_born']))
        if errors:
            flash(str(errors))
            return make_response(
                redirect(request.headers.get("Referer"))
            )

        children = ChildrenDeserialize.deserialize(request.form, DES_FOR_EDIT_CHILD)
        children.id = children_id
        children.parents = Parents(account_main=AccountMain(id=auth_account_main_id))

        children, err = ChildrenService.edit_child(children)
        if err:
            flash(err)
            return make_response(
                redirect(request.headers.get("Referer"))
            )

        flash(SuccessEnum.update)
        resp = make_response(
            redirect(
                url_for('parents/private_office.progress', children_id=children_id)
            )
        )
        return resp


@private_office_parents.route('/add_child', methods=['POST'])
@get_parent_id_and_acc_id_with_confirmed_email
def add_child(auth_account_main_id: int, parent_id: int):
    if request.method == 'POST':
        errors = AddChildrenSchema().validate(dict(name=request.form['name'],
                                                   surname=request.form['surname'],
                                                   date_born=request.form['date_born']))
        if errors:
            flash(str(errors))
            return make_response(
                redirect(request.headers.get("Referer"))
            )

        children = ChildrenDeserialize.deserialize(request.form, DES_FOR_ADD_CHILD)
        children.parents = Parents(id=parent_id)

        children, err = ChildrenService.add_child(children)
        if err:
            flash(err)
            return make_response(
                redirect(request.headers.get("Referer"))
            )

        response = make_response(redirect(url_for("parents/private_office.index")))
        flash(SuccessEnum.update)
        return response

