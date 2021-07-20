from typing import List

from portfolio.internal.biz.deserializers.base_deserializer import BaseDeserializer
from portfolio.internal.biz.deserializers.children_organisation import ChildrenOrganisationDeserializer, \
    DES_FROM_DB_GET_DETAIL_LEARNER
from portfolio.internal.biz.deserializers.events import EventsDeserializer, DES_FROM_DB_GET_DETAIL_EVENT
from portfolio.models.children_organisation import ChildrenOrganisation
from portfolio.models.events_child import EventsChild
from portfolio.models.organisation import Organisation

DES_FROM_DB_GET_EVENTS = "des-from-db-get-active-events"
DES_FROM_DB_GET_INFO_CHILD_ORGANISATION = "des-from-db-get-info-child-organisation"


class EventsChildDeserializer(BaseDeserializer):

    @classmethod
    def _get_deserializer(cls, format_des: str):
        if format_des == DES_FROM_DB_GET_EVENTS:
            return cls._des_from_db_get_events
        elif format_des == DES_FROM_DB_GET_INFO_CHILD_ORGANISATION:
            return cls._des_from_db_get_info_child_organisation
        else:
            raise TypeError

    @staticmethod
    def _des_from_db_get_events(data):
        return [
            EventsChild(
                id=event.get('events_child_id'),
                status=event.get('events_child_status'),
                events=EventsDeserializer.deserialize(event, DES_FROM_DB_GET_DETAIL_EVENT),
                children_organisation=ChildrenOrganisation(organisation=Organisation(name=event.get('organisation_name'),
                                                                                     login=event.get('organisation_login')))
            )
            for event in data
        ]

    @staticmethod
    def _des_from_db_get_info_child_organisation(data) -> List[EventsChild]:
        return [
            EventsChild(
                id=row['events_child_id'],
                status=row['events_child_status'],
                events=EventsDeserializer.deserialize(row, DES_FROM_DB_GET_DETAIL_EVENT),
                children_organisation=ChildrenOrganisationDeserializer.deserialize(row, DES_FROM_DB_GET_DETAIL_LEARNER)
            )
            for row in data
        ]
