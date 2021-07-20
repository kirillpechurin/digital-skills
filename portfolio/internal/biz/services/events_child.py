from portfolio.internal.biz.dao.achievements_child import AchievementsChildDao
from portfolio.internal.biz.dao.events_child import EventsChildDao
from portfolio.models.activity_child import ActivityChild
from portfolio.models.children_organisation import ChildrenOrganisation
from portfolio.models.events_child import EventsChild


class EventsChildService:

    @staticmethod
    def get_completed_events_by_child_id(events_child: EventsChild):
        list_completed_events_child, err = EventsChildDao().get_completed_events_by_child_id(events_child.children_organisation.children.id)
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
