from typing import List, Dict

from portfolio.internal.biz.serializers.achievements import AchievementsSerializer, SER_FOR_DETAIL_ACHIEVEMENT
from portfolio.internal.biz.serializers.base_serializer import BaseSerializer
from portfolio.models.events import Events

SER_FOR_DETAIL_EVENTS = 'ser-for-detail-events'
SER_FOR_DETAIL_EVENTS_ACHIEVEMENTS = 'ser-for-detail-events-achievements'
SER_FOR_LIST_EVENTS = 'ser-for-list-events'
SER_FOR_DETAIL_EVENTS_FOR_DATE = 'ser-for-detail-events-for-date'


class EventsSerializer(BaseSerializer):

    @classmethod
    def _get_serializer(cls, format_ser: str):
        if format_ser == SER_FOR_DETAIL_EVENTS:
            return cls._ser_for_detail_events
        elif format_ser == SER_FOR_LIST_EVENTS:
            return cls._ser_for_list_events
        elif format_ser == SER_FOR_DETAIL_EVENTS_ACHIEVEMENTS:
            return cls._ser_for_detail_events_achievements
        elif format_ser == SER_FOR_DETAIL_EVENTS_FOR_DATE:
            return cls._ser_for_detail_events_for_date

    @staticmethod
    def _ser_for_detail_events(events: Events):
        return {
            "id": events.id,
            "type": events.type,
            "name": events.name,
            "date_event": events.date_event,
            "hours": events.hours,
            "skill": events.skill,
        }

    @staticmethod
    def _ser_for_list_events(list_events: List[Events]):
        return [
            {
                "id": events.id,
                "type": events.type,
                "name": events.name,
                "date_event": events.date_event,
                "hours": events.hours,
                "skill": events.skill,
            }
            for events in list_events
        ]

    @staticmethod
    def _ser_for_detail_events_achievements(dict_for_ser: Dict[str, object or List[object]]):
        return {
            "event": EventsSerializer.serialize(dict_for_ser.get('event'), SER_FOR_DETAIL_EVENTS),
            "achievements": [
                AchievementsSerializer.serialize(achiev, SER_FOR_DETAIL_ACHIEVEMENT)
            for achiev in dict_for_ser.get('achievements')
            ]
        }

    @staticmethod
    def _ser_for_detail_events_for_date(dict_for_ser: Dict[str, object or List[object]]):
        return {
            "events": [
                EventsSerializer.serialize(event, SER_FOR_DETAIL_EVENTS)
                for event in dict_for_ser.get('events_for_date')
            ],
            "calendar": [
                [
                    week_day.day for week_day in week
                ]
                for week in dict_for_ser.get('calendar')
            ],
            "month_str": dict_for_ser.get('month_str'),
            "calendar_date": dict_for_ser.get('calendar_date')
        }
