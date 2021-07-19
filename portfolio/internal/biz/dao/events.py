import datetime

from sqlalchemy import and_

from portfolio.internal.biz.dao.base_dao import BaseDao
from portfolio.internal.biz.deserializers.events import EventsDeserializer, DES_FROM_DB_ALL_EVENTS_ORG
from portfolio.models.events import Events


class EventsDao(BaseDao):

    def get_active_events_by_org_id(self, organisation_id):
        with self.session() as sess:
            data = sess.query(
                Events._id.label('events_id'),
                Events._type.label('events_type'),
                Events._name.label('events_name'),
                Events._date_event.label('events_date_event'),
                Events._hours.label('events_hours'),
                Events._skill.label('events_skill'),
                Events._organisation_id.label('events_organisation_id'),
            ).where(and_(
                Events._organisation_id == organisation_id,
                Events._date_event > datetime.datetime.utcnow()

            )
            )
        if not data:
            return None, None
        return EventsDeserializer.deserialize(data, DES_FROM_DB_ALL_EVENTS_ORG), None