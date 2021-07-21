from typing import List, Dict

from portfolio.internal.biz.serializers.base_serializer import BaseSerializer
from portfolio.internal.biz.serializers.children import ChildrenSerializer, SER_FOR_DETAIL_CHILD
from portfolio.internal.biz.serializers.employee import EmployeeSerializer, SER_FOR_DETAIL_EMPLOYEE
from portfolio.internal.biz.serializers.events import EventsSerializer, SER_FOR_DETAIL_EVENTS
from portfolio.models.account_role import AccountRole
from portfolio.models.organisation import Organisation

SER_FOR_LIST_ORGANISATION = 'ser-for-list-organisation'
SER_FOR_DETAIL_ORGANISATION = 'ser-for-detail_organisation'
SER_FOR_DETAIL_EVENT = 'ser-for-detail-event'
SER_FOR_DETAIL_ORGANISATION_EMPLOYEE = 'ser-for-detail-organisation-employee'
SER_FOR_DETAIL_ORGANISATION_FOR_PARENTS = 'ser-for-detail-organisation-for-parents'


class OrganisationSerializer(BaseSerializer):

    @classmethod
    def _get_serializer(cls, format_ser: str):
        if format_ser == SER_FOR_LIST_ORGANISATION:
            return cls._ser_for_list_organisation
        elif format_ser == SER_FOR_DETAIL_ORGANISATION:
            return cls._ser_for_detail_organisation
        elif format_ser == SER_FOR_DETAIL_EVENT:
            return cls._ser_for_detail_event
        elif format_ser == SER_FOR_DETAIL_ORGANISATION_EMPLOYEE:
            return cls._ser_for_detail_organisation_employee
        elif format_ser == SER_FOR_DETAIL_ORGANISATION_FOR_PARENTS:
            return cls._ser_for_detail_organisation_for_parents

    @staticmethod
    def _ser_for_list_organisation(list_organisations: List[Organisation]):
        return [
            {
                "id": org.id,
                "name": org.name,
                "login": org.login,
                "photo_link": org.photo_link,
                "description": org.description,
            }
            for org in list_organisations
        ]

    @staticmethod
    def _ser_for_detail_organisation(dict_for_ser: Dict[str, object or int]):
        return {
            "organisation": {
                "id": dict_for_ser.get('organisation').id,
                "name": dict_for_ser.get('organisation').name,
                "login": dict_for_ser.get('organisation').login,
                "photo_link": dict_for_ser.get('organisation').photo_link,
                "description": dict_for_ser.get('organisation').description,
            },
            "employees": [
                EmployeeSerializer.serialize(employee, SER_FOR_DETAIL_EMPLOYEE)
                for employee in dict_for_ser.get('list_employee')
            ],
            "active_events": [
                EventsSerializer.serialize(events, SER_FOR_DETAIL_EVENTS)
                for events in dict_for_ser.get('list_active_events')
            ],
            "count_employee": dict_for_ser.get("count_employee"),
            "count_events": dict_for_ser.get('count_events')
        }

    @staticmethod
    def _ser_for_detail_event(dict_for_ser: Dict[str, object or List[object]]):
        return {
            "event": EventsSerializer.serialize(dict_for_ser.get('event'), SER_FOR_DETAIL_EVENTS),
            "list_children": [
                ChildrenSerializer.serialize(child, SER_FOR_DETAIL_CHILD)
                for child in dict_for_ser.get('list_children')
            ]
        }

    @staticmethod
    def _ser_for_detail_organisation_employee(dict_for_ser: Dict[str, object or List[object]]):
        return {
            "organisation": {
                "id": dict_for_ser.get('info_organisation').id,
                "name": dict_for_ser.get('info_organisation').name,
                "login": dict_for_ser.get('info_organisation').login,
                "photo_link": dict_for_ser.get('info_organisation').photo_link,
                "description": dict_for_ser.get('info_organisation').description,
            },
            "employees": [
                EmployeeSerializer.serialize(employee, SER_FOR_DETAIL_EMPLOYEE)
                for employee in dict_for_ser.get('list_employee')
            ]
        }

    @staticmethod
    def _ser_for_detail_organisation_for_parents(organisation: Organisation):
        return {
            "id": organisation.id,
            "name": organisation.name
        }
