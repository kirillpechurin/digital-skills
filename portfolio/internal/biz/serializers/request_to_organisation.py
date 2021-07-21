from typing import List

from portfolio.internal.biz.serializers.base_serializer import BaseSerializer
from portfolio.internal.biz.serializers.events import EventsSerializer, SER_FOR_DETAIL_EVENTS
from portfolio.models.request_to_organisation import RequestToOrganisation

SER_FOR_LIST_REQUESTS = 'ser-for-list-requests'
SER_FOR_DETAIL_REQUEST = 'ser-for-detail-request'


class RequestToOrganisationSerializer(BaseSerializer):

    @classmethod
    def _get_serializer(cls, format_ser: str):
        if format_ser == SER_FOR_LIST_REQUESTS:
            return cls._ser_for_list_requests
        elif format_ser == SER_FOR_DETAIL_REQUEST:
            return cls._ser_for_detail_request

    @staticmethod
    def _ser_for_list_requests(list_requests: List[RequestToOrganisation]):
        return [
            {
                "request_to_organisation": {
                    "id": req.id,
                    "status": req.status
                },
                "parents": {
                    "id": req.parents.id,
                    "name": req.parents.name,
                    "surname": req.parents.surname,
                },
                "children": {
                    "id": req.children.id,
                    "name": req.children.name,
                    "surname": req.children.surname,
                    "date_born": req.children.date_born,
                },
                "events": {
                    "id": req.events.id,
                    "name": req.events.name,
                    "date_event": req.events.date_event,
                }
            }
            for req in list_requests
        ]

    @staticmethod
    def _ser_for_detail_request(request: RequestToOrganisation):
        return {
            "id": request.id,
            "status": request.status,
            "parents": {
                "id": request.parents.id,
                "name": request.parents.name,
                "surname": request.parents.surname,
            },
            "children": {
                "id": request.children.id,
                "name": request.children.name,
                "surname": request.children.surname,
                "date_born": request.children.date_born,
            },
            "event": EventsSerializer.serialize(request.events, SER_FOR_DETAIL_EVENTS)
        }
