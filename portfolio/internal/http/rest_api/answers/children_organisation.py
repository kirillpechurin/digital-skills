from typing import List, Dict

from flask import jsonify

from portfolio.internal.biz.serializers.children_organisation import ChildrenOrganisationSerializer, \
    SER_FOR_LIST_LEARNERS, SER_FOR_DETAIL_LEARNER
from portfolio.models.children_organisation import ChildrenOrganisation


def get_response_list_learners(list_learners: List[ChildrenOrganisation]):
    return jsonify(ChildrenOrganisationSerializer.serialize(list_learners, SER_FOR_LIST_LEARNERS))


def get_response_detail_learner(dict_for_ser: Dict[str, object or List[object]]):
    return jsonify(ChildrenOrganisationSerializer.serialize(dict_for_ser, SER_FOR_DETAIL_LEARNER))
