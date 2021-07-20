from datetime import date, timedelta
import random

from portfolio.internal.biz.dao.achievements_child import AchievementsChildDao
from portfolio.internal.biz.dao.events_child import EventsChildDao
from portfolio.models.activity_child import ActivityChild
from portfolio.models.children_organisation import ChildrenOrganisation
from portfolio.models.events_child import EventsChild


COLORS_SKILL = [
    "primary",
    "secondary",
    "success",
    "danger",
    "warning",
    "info"
]


class EventsChildService:

    @staticmethod
    def get_completed_events_by_child_id(events_child: EventsChild):
        list_completed_events_child, err = EventsChildDao().get_completed_events_by_child_id(events_child.children_organisation.children.id)
        if err:
            return None, err
        return list_completed_events_child, None

    @staticmethod
    def get_completed_events_by_child_id_with_date(events_child: EventsChild, gap_for_skill):
        list_completed_events_child, err = EventsChildDao().get_completed_events_by_child_id_with_date(events_child.children_organisation.children.id, gap_for_skill)
        if err:
            return None, err
        return list_completed_events_child, None

    @staticmethod
    def get_active_events_by_child_id(events_child: EventsChild):
        list_active_events_child, err = EventsChildDao().get_active_events_by_child_id(events_child.children_organisation.children.id)
        if err:
            return None, err
        return list_active_events_child, None

    @staticmethod
    def get_by_children_organisation_id(children_organisation: ChildrenOrganisation):
        list_active_events, err = EventsChildDao().get_active_events_by_child_organisation_id(children_organisation.id)
        if err:
            return None, err

        list_completed_events, err = EventsChildDao().get_completed_events_by_child_organisation_id(children_organisation.id)
        if err:
            return None, err

        list_achievements_child, err = AchievementsChildDao().get_by_children_organisation_id(children_organisation.id)
        if err:
            return None, err

        activity_child = ActivityChild(
            list_completed_events=list_completed_events,
            list_active_events=list_active_events,
            list_achievements_child=list_achievements_child
        )
        return activity_child, None

    @staticmethod
    def update_status(events_child: EventsChild):
        events_child, err = EventsChildDao().update_status(events_child)
        if err:
            return None, err
        return events_child, None

    @staticmethod
    def update_hours(events_child: EventsChild):
        events_child, err = EventsChildDao().update_hours(events_child)
        if err:
            return None, err
        return events_child, None

    @staticmethod
    def get_statistic_by_skill(events_child: EventsChild, gap_for_skill: str or date):
        if gap_for_skill == 'all_time':
            gap_for_skill = date.min
        elif gap_for_skill == 'year':
            gap_for_skill = date.today() - timedelta(days=365)
        elif gap_for_skill == 'half_year':
            gap_for_skill = date.today() - timedelta(days=182)
        elif gap_for_skill == 'month':
            gap_for_skill = date.today() - timedelta(days=30)
        elif isinstance(gap_for_skill, date):
            pass
        else:
            raise TypeError

        list_completed_events, err = EventsChildService.get_completed_events_by_child_id_with_date(events_child, gap_for_skill)
        if err:
            return None, err
        if not list_completed_events:
            return None, None
        unique_skill = list(set([item.events.skill for item in list_completed_events]))
        sum_hours = sum([item.events.hours for item in list_completed_events])
        dict_by_unique_skill = {}
        for skill in unique_skill:
            dict_by_unique_skill[skill] = {
                "hours": 0,
                "percent": 0.00,
                "color": ""
            }
        for event in list_completed_events:
            dict_by_unique_skill[event.events.skill]['hours'] += event.events.hours
        list_colors = COLORS_SKILL.copy()
        for num, key in enumerate(dict_by_unique_skill):
            percent = dict_by_unique_skill[key]['hours'] * 100 / sum_hours
            dict_by_unique_skill[key]["percent"] = float("{0:.2f}".format(percent))
            dict_by_unique_skill[key]['color'] = random.choice(list_colors)
        return dict_by_unique_skill, None

    @staticmethod
    def get_statistic_by_org(events_child: EventsChild, gap_for_org: str or date):
        if gap_for_org == 'all_time':
            gap_for_org = date.min
        elif gap_for_org == 'year':
            gap_for_org = date.today() - timedelta(days=365)
        elif gap_for_org == 'half_year':
            gap_for_org = date.today() - timedelta(days=182)
        elif gap_for_org == 'month':
            gap_for_org = date.today() - timedelta(days=30)
        elif isinstance(gap_for_org, date):
            pass
        else:
            raise TypeError
        list_completed_events, err = EventsChildService.get_completed_events_by_child_id_with_date(events_child,
                                                                                                   gap_for_org)
        if err:
            return None, err
        if not list_completed_events:
            return None, None
        unique_org = list(set([event.children_organisation.organisation.login for event in list_completed_events]))
        sum_hours = sum([item.events.hours for item in list_completed_events])
        dict_by_unique_org = {}
        for org in unique_org:
            dict_by_unique_org[org] = {
                "name": '',
                "hours": 0,
                "percent": 0.00,
                "color": ""
            }
        for event in list_completed_events:
            dict_by_unique_org[event.children_organisation.organisation.login]['hours'] += event.events.hours
            dict_by_unique_org[event.children_organisation.organisation.login]['name'] = event.children_organisation.organisation.name

        list_colors = COLORS_SKILL.copy()
        for num, key in enumerate(dict_by_unique_org):
            percent = dict_by_unique_org[key]['hours'] * 100 / sum_hours
            dict_by_unique_org[key]["percent"] = float("{0:.2f}".format(percent))
            dict_by_unique_org[key]['color'] = random.choice(list_colors)
        return dict_by_unique_org, None

    @staticmethod
    def get_statistic_focus_time(events_child: EventsChild):
        gap_focus = date.today() - timedelta(days=7)
        list_completed_events, err = EventsChildService.get_completed_events_by_child_id_with_date(events_child, gap_focus)
        if err:
            return None, err
        if not list_completed_events:
            return None, None
        unique_skill = list(set([item.events.skill for item in list_completed_events]))
        dict_by_max_skill = {}
        for skill in unique_skill:
            dict_by_max_skill[skill] = {
                "event_type": None,
                "event_name": None,
                "skill": None,
                "hours": 0,
            }
        for event in list_completed_events:
            dict_by_max_skill[event.events.skill]['hours'] += event.events.hours
            dict_by_max_skill[event.events.skill]['event_name'] = event.events.name
            dict_by_max_skill[event.events.skill]['event_type'] = event.events.type
            dict_by_max_skill[event.events.skill]['skill'] = event.events.skill
        max_focus_event = {
            "hours": 0
        }
        for key in dict_by_max_skill:
            if dict_by_max_skill[key]['hours'] > max_focus_event['hours']:
                max_focus_event = dict_by_max_skill[key]
        return max_focus_event, None