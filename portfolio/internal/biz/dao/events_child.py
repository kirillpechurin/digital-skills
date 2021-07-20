from sqlalchemy import and_, insert

from portfolio.internal.biz.dao.base_dao import BaseDao
from portfolio.internal.biz.deserializers.events_child import DES_FROM_DB_GET_ACTIVE_EVENTS, EventsChildDeserializer, \
    DES_FROM_DB_GET_EVENTS
from portfolio.models.children_organisation import ChildrenOrganisation
from portfolio.models.events import Events
from portfolio.models.events_child import EventsChild
from portfolio.models.organisation import Organisation
from portfolio.models.request_to_organisation import RequestToOrganisation


class EventsChildDao(BaseDao):

    def get_completed_events_by_child_id(self, children_id: int):
        with self.session() as sess:
            data = sess.query(
                EventsChild._id.label('events_child_id'),
                EventsChild._status.label('events_child_status'),
                EventsChild._hours_event.label('events_child_hours_event'),
                Events._id.label('events_id'),
                Events._type.label('events_type'),
                Events._name.label('events_name'),
                Events._date_event.label('events_date_event'),
                Events._skill.label('events_skill'),
                Organisation._name.label('organisation_name')
            ).join(
                EventsChild._events
            ).join(
                EventsChild._children_organisation
            ).join(
                ChildrenOrganisation._organisation
            ).where(and_(EventsChild._status is True, ChildrenOrganisation._children_id == children_id)).all()
        if not data:
            return None, None
        return EventsChildDeserializer.deserialize(data, DES_FROM_DB_GET_EVENTS), None

    def get_active_events_by_child_id(self, children_id):
        with self.session() as sess:
            data = sess.query(
                EventsChild._id.label('events_child_id'),
                EventsChild._status.label('events_child_status'),
                EventsChild._hours_event.label('events_child_hours_event'),
                Events._id.label('events_id'),
                Events._type.label('events_type'),
                Events._name.label('events_name'),
                Events._date_event.label('events_date_event'),
                Events._skill.label('events_skill'),
                Organisation._name.label('organisation_name')
            ).join(
                EventsChild._events
            ).join(
                EventsChild._children_organisation
            ).join(
                ChildrenOrganisation._organisation
            ).where(and_(EventsChild._status is False, ChildrenOrganisation._children_id == children_id)).all()
        if not data:
            return None, None
        return EventsChildDeserializer.deserialize(data, DES_FROM_DB_GET_EVENTS), None

    def add_by_request(self, events_child: EventsChild):
        sql = insert(
            EventsChild
        ).values(
            children_organisation_id=events_child.children_organisation.id,
            hours_event=events_child.events.hours,
            events_id=events_child.events.id,
        ).returning(
            EventsChild._id.label('events_child_id'),
            EventsChild._created_at.label('events_child_created_at'),
            EventsChild._edited_at.label('events_child_edited_at'),
        )

        sess = self.sess_transaction
        row = sess.execute(sql).first()
        sess.commit()

        events_child.id = row['events_child_id']
        events_child.created_at = row['events_child_created_at']
        events_child.edited_at = row['events_child_edited_at']
        return events_child, None
