from typing import List

from internal.biz.deserializers.base_deserializer import BaseDeserializer
from models.events import Events

DES_FROM_DB_GET_DETAIL_EVENT = "des-from-db-get-detail-event"
DES_FROM_DB_EVENTS_ORG = 'des-from-db-events-org'
DES_FOR_ADD_EVENT = 'des-for-add-event'
DES_FOR_EDIT_EVENT = 'des-for-edit-event'
DES_FROM_DB_INFO_EVENTS = 'des-from-db-info-events'


class EventsDeserializer(BaseDeserializer):

    @classmethod
    def _get_deserializer(cls, format_des: str):
        if format_des == DES_FROM_DB_GET_DETAIL_EVENT:
            return cls._des_from_db_get_detail_event
        elif format_des == DES_FROM_DB_EVENTS_ORG:
            return cls._des_from_db_events_org
        elif format_des == DES_FOR_ADD_EVENT:
            return cls._des_for_add_event
        elif format_des == DES_FROM_DB_INFO_EVENTS:
            return cls._des_from_db_info_events
        elif format_des == DES_FOR_EDIT_EVENT:
            return cls._des_for_edit_event

    @staticmethod
    def _des_for_add_event(req_form) -> Events:
        return Events(
            type=req_form.get('type'),
            name=req_form.get('name'),
            date_event=req_form.get('date_event'),
            hours=req_form.get('hours'),
            skill=req_form.get('skill')
        )

    @staticmethod
    def _des_from_db_get_detail_event(row) -> Events:
        return Events(
            id=row.get('events_id'),
            type=row.get('events_type'),
            name=row.get('events_name'),
            date_event=row.get('events_date_event'),
            hours=row.get('events_hours'),
            skill=row.get('events_skill')
        )

    @staticmethod
    def _des_from_db_events_org(data) -> List[Events]:
        return [
            Events(
            id=row.get('events_id'),
            type=row.get('events_type'),
            name=row.get('events_name'),
            date_event=row.get('events_date_event'),
            hours=row.get('events_hours'),
            skill=row.get('events_skill')
            )
            for row in data
        ]

    @staticmethod
    def _des_from_db_info_events(row) -> Events:
        return Events(
            id=row.get('events_id'),
            name=row.get('events_name'),
            date_event=row.get('events_date_event'),
        )

    @staticmethod
    def _des_for_edit_event(req_form):
        return Events(
            type=req_form.get('type') if req_form.get('type') else '-1',
            name=req_form.get('name') if req_form.get('name') else '-1',
            date_event=req_form.get('date_event') if req_form.get('date_event') else '-1',
            hours=req_form.get('hours') if req_form.get('hours') else -1,
            skill=req_form.get('skill') if req_form.get('skill') else '-1'
        )
