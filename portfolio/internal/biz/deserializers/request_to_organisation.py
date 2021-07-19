from typing import List

from portfolio.internal.biz.deserializers.base_deserializer import BaseDeserializer
from portfolio.internal.biz.deserializers.children import ChildrenDeserialize, DES_FROM_DB_INFO_CHILDREN
from portfolio.internal.biz.deserializers.events import EventsDeserializer, DES_FROM_DB_INFO_EVENTS, \
    DES_FROM_DB_GET_DETAIL_EVENT
from portfolio.internal.biz.deserializers.parents import ParentsDeserializer, DES_FROM_DB_INFO_PARENTS
from portfolio.models.request_to_organisation import RequestToOrganisation

DES_FROM_DB_ALL_ACTIVE_REQUESTS = 'des-from-db-all-active-requests'
DES_FROM_DB_DETAIL_REQUEST = 'des-from-db-detail-requests'


class RequestToOrganisationDeserializer(BaseDeserializer):

    @classmethod
    def _get_deserializer(cls, format_des: str):
        if format_des == DES_FROM_DB_ALL_ACTIVE_REQUESTS:
            return cls._des_from_db_all_active_requests
        elif format_des == DES_FROM_DB_DETAIL_REQUEST:
            return cls._des_from_db_detail_request
        else:
            raise TypeError

    @staticmethod
    def _des_from_db_all_active_requests(data) -> List[RequestToOrganisation]:
        return [
            RequestToOrganisation(
                id=row['request_to_organisation_id'],
                parents=ParentsDeserializer.deserialize(row, DES_FROM_DB_INFO_PARENTS),
                events=EventsDeserializer.deserialize(row, DES_FROM_DB_INFO_EVENTS),
                children=ChildrenDeserialize.deserialize(row, DES_FROM_DB_INFO_CHILDREN),
                status=row['request_to_organisation_status']
            )
            for row in data
        ]

    @staticmethod
    def _des_from_db_detail_request(row):
        return RequestToOrganisation(
            id=row['request_to_organisation_id'],
            parents=ParentsDeserializer.deserialize(row, DES_FROM_DB_INFO_PARENTS),
            events=EventsDeserializer.deserialize(row, DES_FROM_DB_GET_DETAIL_EVENT),
            children=ChildrenDeserialize.deserialize(row, DES_FROM_DB_INFO_CHILDREN),
            status=row['request_to_organisation_status']
        )
