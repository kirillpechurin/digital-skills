from typing import List

from flask import jsonify

from portfolio.internal.biz.serializers.request_to_organisation import RequestToOrganisationSerializer, \
    SER_FOR_LIST_REQUESTS, SER_FOR_DETAIL_REQUEST
from portfolio.models.request_to_organisation import RequestToOrganisation


def get_response_list_requests(list_request: List[RequestToOrganisation]):
    return jsonify(RequestToOrganisationSerializer.serialize(list_request, SER_FOR_LIST_REQUESTS))


def get_response_detail_request(request: RequestToOrganisation):
    return jsonify(RequestToOrganisationSerializer.serialize(request, SER_FOR_DETAIL_REQUEST))