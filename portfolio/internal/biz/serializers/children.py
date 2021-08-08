from typing import List, Dict

from portfolio.internal.biz.serializers.base_serializer import BaseSerializer
from portfolio.internal.biz.serializers.events_child import EventsChildSerializer, SER_FOR_DETAIL_EVENTS_CHILD
from portfolio.models.children import Children

SER_FOR_DETAIL_CHILD = 'ser-for-detail-child'
SER_FOR_DETAIL_CHILDREN = 'ser-for-detail-children'
SER_FOR_LIST_CHILDREN = 'ser-for-list-children'
SER_FOR_DETAIL_CHILDREN_WITH_EVENTS = 'ser-for-detail-children-with-events'
SER_FOR_DETAIL_CHILDREN_PROGRESS = 'ser-for-detail-children-progress'


class ChildrenSerializer(BaseSerializer):

    @classmethod
    def _get_serializer(cls, format_ser: str):
        if format_ser == SER_FOR_DETAIL_CHILD:
            return cls._ser_for_detail_child
        elif format_ser == SER_FOR_DETAIL_CHILDREN:
            return cls._ser_for_detail_children
        elif format_ser == SER_FOR_DETAIL_CHILDREN_WITH_EVENTS:
            return cls._ser_for_detail_children_with_events
        elif format_ser == SER_FOR_LIST_CHILDREN:
            return cls._ser_for_list_children
        elif format_ser == SER_FOR_DETAIL_CHILDREN_PROGRESS:
            return cls._ser_for_detail_children_progress

    @staticmethod
    def _ser_for_detail_child(child: Children):
        return {
            "id": child.id,
            "name": child.name,
            "surname": child.surname,
            "date_born": child.date_born,
            "parents": {
                "id": child.parents.id,
            }
        }

    @staticmethod
    def _ser_for_detail_children(child: Children):
        return {
            "id": child.id,
            "name": child.name,
            "surname": child.surname,
            "date_born": child.date_born,
        }

    @staticmethod
    def _ser_for_list_children(list_children: List[Children]):
        return [
            {
                "id": child.id,
                "name": child.name,
                "surname": child.surname,
                "date_born": child.date_born,
            }
            for child in list_children
        ]

    @staticmethod
    def _ser_for_detail_children_with_events(list_for_ser: List[Dict[str, object or List[object]]]):
        return [
            {
                "children": ChildrenSerializer.serialize(child.get('children_info'), SER_FOR_DETAIL_CHILDREN),
                "events_child": EventsChildSerializer.serialize(child.get('events_info'), SER_FOR_DETAIL_EVENTS_CHILD),
            }
            for child in list_for_ser
        ]

    @staticmethod
    def _ser_for_detail_children_progress(dict_for_ser: Dict[str, object or List[object]]):
        return {
            "children": ChildrenSerializer.serialize(dict_for_ser.get('children'), SER_FOR_DETAIL_CHILDREN),
            "active_events": [
                EventsChildSerializer.serialize(event, SER_FOR_DETAIL_EVENTS_CHILD)
                for event in dict_for_ser.get('active_events')
            ],
            "complete_events": [
                EventsChildSerializer.serialize(event, SER_FOR_DETAIL_EVENTS_CHILD)
                for event in dict_for_ser.get('complete_events')
            ],
            "list_organisation_for_child": [
                {
                    "id": org.id,
                    "name": org.name
                }
                for org in dict_for_ser.get('list_organisation_for_child')
            ],
        }
