from datetime import date

from portfolio.internal.biz.dao.events import EventsDao
from portfolio.models.events import Events


class EventsService:

    @staticmethod
    def update_event(event: Events):
        event, err = EventsDao().update(event.id, event)
        if err:
            return None, err
        return event, None

    @staticmethod
    def get_active_events_by_organisation_id(organisation_id: int):
        events, err = EventsDao().get_active_events_by_org_id(organisation_id)
        if err:
            return None, err
        return events, None

    @staticmethod
    def get_by_events_id(events: Events):
        event, err = EventsDao().get_by_id(events.id)
        if err:
            return None, err
        return event, None

    @staticmethod
    def add_event(events: Events):
        event, err = EventsDao().add(events)
        if err:
            return None, err
        return event, None

    @staticmethod
    def get_all_events_by_organisation_id(organisation_id: int):
        list_events, err = EventsDao().get_by_organisation_id(organisation_id)
        if err:
            return None, err
        return list_events, None

    @staticmethod
    def get_events_by_date(organisation_id: int, calendar_date: date):
        list_events, err = EventsDao().get_by_organisation_id_with_date(organisation_id, calendar_date)
        if err:
            return None, err
        return list_events, None