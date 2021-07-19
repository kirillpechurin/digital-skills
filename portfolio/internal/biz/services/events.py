from portfolio.internal.biz.dao.events import EventsDao
from portfolio.models.events import Events


class EventsService:

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
