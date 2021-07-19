from portfolio.internal.biz.dao.events import EventsDao


class EventsService:

    @staticmethod
    def get_active_events_by_organisation_id(organisation_id: int):
        events, err = EventsDao().get_active_events_by_org_id(organisation_id)
        if err:
            return None, err
        return events, None
