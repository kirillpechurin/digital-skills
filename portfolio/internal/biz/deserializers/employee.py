from portfolio.internal.biz.deserializers.base_deserializer import BaseDeserializer
from portfolio.models.employee import Employee

DES_FROM_DB_ALL_EMPLOYEE = "des-from-db-all-employee"


class EmployeeDeserializer(BaseDeserializer):

    @classmethod
    def _get_deserializer(cls, format_des: str):
        if format_des == DES_FROM_DB_ALL_EMPLOYEE:
            return cls._des_from_db_all_employee

    @staticmethod
    def _des_from_db_all_employee(data):
        return [
            Employee(
                id=row.get('teacher_id'),
                login=row.get('teacher_login'),
                name=row.get('teacher_name'),
                surname=row.get('teacher_surname'),
                specialty=row.get('teacher_specialty'),
            ) for row in data
        ]
