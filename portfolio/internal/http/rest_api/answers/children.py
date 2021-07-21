from typing import List, Dict

from flask import jsonify

from portfolio.internal.biz.serializers.children import ChildrenSerializer, SER_FOR_DETAIL_CHILDREN_WITH_EVENTS, \
    SER_FOR_LIST_CHILDREN, SER_FOR_DETAIL_CHILDREN_PROGRESS
from portfolio.models.children import Children


def get_response_list_children_and_events(list_for_ser: List[Dict[str, object or List[object]]]):
    return jsonify(ChildrenSerializer.serialize(list_for_ser, SER_FOR_DETAIL_CHILDREN_WITH_EVENTS))


def get_response_list_children(list_children: List[Children]):
    return jsonify(ChildrenSerializer.serialize(list_children, SER_FOR_LIST_CHILDREN))


def get_response_detail_children(dict_for_ser: Dict[str, object or List[object]]):
    return jsonify(ChildrenSerializer.serialize(dict_for_ser, SER_FOR_DETAIL_CHILDREN_PROGRESS))