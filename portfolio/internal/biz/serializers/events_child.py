from portfolio.internal.biz.serializers.base_serializer import BaseSerializer
from portfolio.internal.biz.serializers.events import EventsSerializer, SER_FOR_DETAIL_EVENTS
from portfolio.models.events_child import EventsChild

SER_FOR_DETAIL_EVENTS_CHILD = 'ser-for-detail-events-child'


class EventsChildSerializer(BaseSerializer):

    @classmethod
    def _get_serializer(cls, format_ser: str):
        if format_ser == SER_FOR_DETAIL_EVENTS_CHILD:
            return cls._ser_for_detail_events_child

    @staticmethod
    def _ser_for_detail_events_child(events_child: EventsChild):
        return {
            "id": events_child.id,
            "status": events_child.status,
            "events": EventsSerializer.serialize(events_child.events, SER_FOR_DETAIL_EVENTS)
        }
