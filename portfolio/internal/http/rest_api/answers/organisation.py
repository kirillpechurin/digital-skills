from typing import Dict, List

from flask import jsonify

from portfolio.internal.biz.serializers.organisation import OrganisationSerializer, SER_FOR_LIST_ORGANISATION, \
    SER_FOR_DETAIL_ORGANISATION, SER_FOR_DETAIL_EVENT, SER_FOR_DETAIL_ORGANISATION_EMPLOYEE
from portfolio.models.organisation import Organisation


def get_response_list_organisations(organisations: Organisation):
    return jsonify(OrganisationSerializer.serialize(organisations, SER_FOR_LIST_ORGANISATION))


def get_response_detail_organisation(dict_for_ser: Dict[str, object or int]):
    return jsonify(OrganisationSerializer.serialize(dict_for_ser, SER_FOR_DETAIL_ORGANISATION))


def get_response_detail_event(dict_for_ser: Dict[str, object]):
    return jsonify(OrganisationSerializer.serialize(dict_for_ser, SER_FOR_DETAIL_EVENT))


def get_response_detail_organisation_employee(dict_for_ser: Dict[str, object or List[object]]):
    return jsonify(OrganisationSerializer.serialize(dict_for_ser, SER_FOR_DETAIL_ORGANISATION_EMPLOYEE))