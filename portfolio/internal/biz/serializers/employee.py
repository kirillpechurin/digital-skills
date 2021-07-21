from typing import List

from portfolio.internal.biz.serializers.base_serializer import BaseSerializer
from portfolio.models.employee import Employee

SER_FOR_DETAIL_EMPLOYEE = 'ser-for-detail-employee'


class EmployeeSerializer(BaseSerializer):

    @classmethod
    def _get_serializer(cls, format_ser: str):
        if format_ser == SER_FOR_DETAIL_EMPLOYEE:
            return cls._ser_for_detail_employee

    @staticmethod
    def _ser_for_detail_employee(employee: Employee):
        return {
            "id": employee.id,
            "login": employee.login,
            "name": employee.name,
            "surname": employee.surname,
            "specialty": employee.specialty,
        }
