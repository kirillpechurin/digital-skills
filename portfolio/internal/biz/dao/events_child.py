from datetime import date

import sqlalchemy
from sqlalchemy import and_, insert

from enums.error.errors_enum import ErrorEnum
from internal.biz.dao.base_dao import BaseDao
from internal.biz.deserializers.events import EventsDeserializer, DES_FROM_DB_EVENTS_ORG
from internal.biz.deserializers.events_child import EventsChildDeserializer, \
    DES_FROM_DB_GET_EVENTS, DES_FROM_DB_GET_INFO_CHILD_ORGANISATION
from models.children import Children
from models.children_organisation import ChildrenOrganisation
from models.events import Events
from models.events_child import EventsChild
from models.organisation import Organisation


class EventsChildDao(BaseDao):

    def get_completed_events_by_child_id(self, children_id: int):
        with self.session() as sess:
            data = sess.query(
                EventsChild._id.label('events_child_id'),
                EventsChild._status.label('events_child_status'),
                EventsChild._hours_event.label('events_hours'),
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
            ).where(
                and_(
                    EventsChild._status == True,
                    ChildrenOrganisation._children_id == children_id
                )
            ).all()
        if not data:
            return None, None
        data = [dict(row) for row in data]
        return EventsChildDeserializer.deserialize(data, DES_FROM_DB_GET_EVENTS), None

    def get_completed_events_by_child_id_with_date(self, children_id: int, gap_for_skill):
        with self.session() as sess:
            data = sess.query(
                EventsChild._id.label('events_child_id'),
                EventsChild._status.label('events_child_status'),
                EventsChild._hours_event.label('events_hours'),
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
            ).where(
                and_(
                    EventsChild._status == True,
                    ChildrenOrganisation._children_id == children_id,
                    Events._date_event > gap_for_skill
                )
            ).all()
        if not data:
            return None, None
        data = [dict(row) for row in data]
        return EventsChildDeserializer.deserialize(data, DES_FROM_DB_GET_EVENTS), None

    def get_active_events_by_child_id(self, children_id):
        with self.session() as sess:
            data = sess.query(
                EventsChild._id.label('events_child_id'),
                EventsChild._status.label('events_child_status'),
                EventsChild._hours_event.label('events_hours'),
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
            ).where(
                and_(
                    EventsChild._status == False,
                    ChildrenOrganisation._children_id == children_id
                )
            ).all()
        if not data:
            return None, None
        data = [dict(row) for row in data]
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
        try:
            row = sess.execute(sql).first()
            sess.commit()
            row = dict(row)
        except sqlalchemy.exc.IntegrityError as exception:
            if str(exception.orig)[48:48 + len("unique_children_organisation")] == 'unique_children_organisation':
                return None, ErrorEnum.events_child_already_exists
            else:
                raise TypeError
        events_child.id = row['events_child_id']
        events_child.created_at = row['events_child_created_at']
        events_child.edited_at = row['events_child_edited_at']
        return events_child, None

    def get_active_events_by_child_organisation_id(self, children_organisation_id: int = None):
        with self.session() as sess:
            data = sess.query(
                EventsChild._id.label('events_child_id'),
                EventsChild._status.label('events_child_status'),
                EventsChild._hours_event.label('events_hours'),
                Events._id.label('events_id'),
                Events._type.label('events_type'),
                Events._name.label('events_name'),
                Events._date_event.label('events_date_event'),
                Events._skill.label('events_skill'),
                ChildrenOrganisation._id.label('children_organisation_id'),
                Children._id.label('children_id'),
                Children._name.label('children_name'),
                Children._surname.label('children_surname'),
                Children._date_born.label('children_date_born'),
                Children._parents_id.label('children_parents_id'),
            ).join(
                EventsChild._events
            ).join(
                EventsChild._children_organisation
            ).join(
                ChildrenOrganisation._children
            ).where(
                and_(
                    EventsChild._status == False,
                    ChildrenOrganisation._id == children_organisation_id
                )
            ).all()
        if not data:
            return None, None
        data = [dict(row) for row in data]
        return EventsChildDeserializer.deserialize(data, DES_FROM_DB_GET_INFO_CHILD_ORGANISATION), None

    def get_completed_events_by_child_organisation_id(self, children_organisation_id: int = None):
        with self.session() as sess:
            data = sess.query(
                EventsChild._id.label('events_child_id'),
                EventsChild._status.label('events_child_status'),
                EventsChild._hours_event.label('events_hours'),
                Events._id.label('events_id'),
                Events._type.label('events_type'),
                Events._name.label('events_name'),
                Events._date_event.label('events_date_event'),
                Events._skill.label('events_skill'),
                ChildrenOrganisation._id.label('children_organisation_id'),
                Children._id.label('children_id'),
                Children._name.label('children_name'),
                Children._surname.label('children_surname'),
                Children._date_born.label('children_date_born'),
                Children._parents_id.label('children_parents_id'),
            ).join(
                EventsChild._events
            ).join(
                EventsChild._children_organisation
            ).join(
                ChildrenOrganisation._children
            ).where(
                and_(
                    EventsChild._status == True,
                    ChildrenOrganisation._id == children_organisation_id
                )
            ).all()
        if not data:
            return None, None
        data = [dict(row) for row in data]
        return EventsChildDeserializer.deserialize(data, DES_FROM_DB_GET_INFO_CHILD_ORGANISATION), None

    def update_status(self, events_child: EventsChild):
        with self.session() as sess:
            events_child_db = sess.query(
                EventsChild
            ).where(
                and_(
                    EventsChild._children_organisation_id == events_child.children_organisation.id,
                    EventsChild._events_id == events_child.events.id
                )
            ).first()
            if not events_child_db:
                return None, ErrorEnum.event_child_not_found
            events_child_db._status = events_child.status
            sess.commit()
        return events_child, None

    def update_hours(self, events_child: EventsChild):
        with self.session() as sess:
            events_child_db = sess.query(
                EventsChild
            ).where(
                and_(
                    EventsChild._children_organisation_id == events_child.children_organisation.id,
                    EventsChild._events_id == events_child.events.id
                )
            ).first()
            if not events_child_db:
                return None, ErrorEnum.event_child_not_found
            events_child_db._hours_event = events_child.hours_event
            sess.commit()
        return events_child, None

    def get_events_by_date(self, children_id: int, calendar_date: date):
        with self.session() as sess:
            data = sess.query(
                Events._id.label('events_id'),
                Events._type.label('events_type'),
                Events._name.label('events_name'),
                Events._date_event.label('events_date_event'),
                Events._skill.label('events_skill'),
            ).join(
                EventsChild._events
            ).join(
                EventsChild._children_organisation
            ).where(
                and_(
                    Events._date_event == calendar_date,
                    ChildrenOrganisation._children_id == children_id
                )
            ).all()
        data = [dict(row) for row in data]
        return EventsDeserializer.deserialize(data, DES_FROM_DB_EVENTS_ORG), None
