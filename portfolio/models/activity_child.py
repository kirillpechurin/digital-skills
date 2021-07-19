from typing import Optional, List

from portfolio.models.achievements_child import AchievementsChild
from portfolio.models.events_child import EventsChild


class ActivityChild:

    def __init__(self,
                 list_active_events: Optional[List[EventsChild]] = None,
                 list_completed_events: Optional[List[EventsChild]] = None,
                 list_achievements_child: Optional[List[AchievementsChild]] = None):
        self.__list_active_events = list_active_events
        self.__list_completed_events = list_completed_events
        self.__list_achievements_child = list_achievements_child

    @property
    def list_completed_events(self):
        return self.__list_completed_events

    @list_completed_events.setter
    def list_completed_events(self, value: List[EventsChild]):
        self.__list_completed_events = value

    @property
    def list_active_events(self):
        return self.__list_active_events

    @list_active_events.setter
    def list_active_events(self, value: List[EventsChild]):
        self.__list_active_events = value

    @property
    def list_achievements_child(self):
        return self.__list_achievements_child

    @list_achievements_child.setter
    def list_achievements_child(self, value: List[AchievementsChild]):
        self.__list_achievements_child = value
