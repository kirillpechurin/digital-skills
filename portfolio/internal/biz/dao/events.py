import datetime
from datetime import datetime as dt

from sqlalchemy import and_, insert

from portfolio.internal.biz.dao.base_dao import BaseDao
from portfolio.internal.biz.deserializers.events import EventsDeserializer, DES_FROM_DB_GET_DETAIL_EVENT, DES_FROM_DB_EVENTS_ORG
from portfolio.models.events import Events


class EventsDao(BaseDao):

    def update(self, event_id: int, event: Events):
        with self.session() as sess:
            events_db = sess.query(Events).where(Events._id == event_id).first()
            created_at = events_db._created_at
            for column in events_db.__dict__:
                if getattr(event, f"{column[1:]}", '-1') != '-1':
                    setattr(events_db, f"{column}", getattr(event, f"{column[1:]}"))
            setattr(events_db, '_edited_at', dt.utcnow())
            setattr(events_db, '_created_at', created_at)
            sess.commit()
        return events_db, None


    def add(self, event: Events):
        sql = insert(
            Events
        ).values(
            type=event.type,
            name=event.name,
            date_event=event.date_event,
            hours=event.hours,
            skill=event.skill,
            organisation_id=event.organisation.id
        ).returning(
            Events._id.label('events_id'),
            Events._created_at.label('events_created_at'),
            Events._edited_at.label('events_edited_at')
        )
        with self.session() as sess:
            row = sess.execute(sql).first()
            sess.commit()
        if not row:
            return None, None
        row = dict(row)
        event.id = row['events_id']
        event.created_at = row['events_created_at']
        event.edited_at = row['events_edited_at']
        return event, None

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
            ).where(
                and_(
                    Events._organisation_id == organisation_id,
                    Events._date_event > datetime.datetime.utcnow()
                )
            )
        if not data:
            return None, None
        data = [dict(row) for row in data]
        return EventsDeserializer.deserialize(data, DES_FROM_DB_EVENTS_ORG), None

    def get_by_id(self, event_id: int):
        if self.sess_transaction:
            row = self.sess_transaction.query(
                Events._id.label("events_id"),
                Events._type.label("events_type"),
                Events._name.label("events_name"),
                Events._date_event.label("events_date_event"),
                Events._hours.label("events_hours"),
                Events._skill.label("events_skill"),
            ).where(Events._id == event_id).first()
            if not row:
                return None, "Данное событие не существует"
            row = dict(row)
            return EventsDeserializer.deserialize(row, DES_FROM_DB_GET_DETAIL_EVENT), None
        with self.session() as sess:
            row = sess.query(
                Events._id.label("events_id"),
                Events._type.label("events_type"),
                Events._name.label("events_name"),
                Events._date_event.label("events_date_event"),
                Events._hours.label("events_hours"),
                Events._skill.label("events_skill"),
            ).where(Events._id == event_id).first()
        if not row:
            return None, "Данное событие не существует"
        row = dict(row)
        return EventsDeserializer.deserialize(row, DES_FROM_DB_GET_DETAIL_EVENT), None

    def get_by_organisation_id(self, organisation_id: int):
        with self.session() as sess:
            data = sess.query(
                Events._id.label("events_id"),
                Events._type.label("events_type"),
                Events._name.label("events_name"),
                Events._date_event.label("events_date_event"),
                Events._hours.label("events_hours"),
                Events._skill.label("events_skill"),
            ).where(Events._organisation_id == organisation_id).all()
        if not data:
            return None, None
        data = [dict(row) for row in data]
        return EventsDeserializer.deserialize(data, DES_FROM_DB_EVENTS_ORG), None
