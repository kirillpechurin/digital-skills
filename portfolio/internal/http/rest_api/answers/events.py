from typing import List, Dict

from flask import jsonify

from portfolio.internal.biz.serializers.events import EventsSerializer, SER_FOR_LIST_EVENTS, \
    SER_FOR_DETAIL_EVENTS_ACHIEVEMENTS
from portfolio.models.events import Events


def get_response_list_events(list_events: List[Events]):
    return jsonify(EventsSerializer.serialize(list_events, SER_FOR_LIST_EVENTS))


def get_response_detail_events(dict_for_ser: Dict[str, object or List[object]]):
    return jsonify(EventsSerializer.serialize(dict_for_ser, SER_FOR_DETAIL_EVENTS_ACHIEVEMENTS))


def get_response_detail_events_for_date(dict_for_ser: Dict[str, object or List[object]]):
    return jsonify(EventsSerializer.serialize(dict_for_ser, SER_FOR_DETAIL_EVENTS_FOR_DATE))