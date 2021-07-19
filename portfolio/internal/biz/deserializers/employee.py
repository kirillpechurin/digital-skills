from portfolio.internal.biz.deserializers.base_deserializer import BaseDeserializer
from portfolio.models.employee import Employee

DES_FROM_DB_ALL_EMPLOYEE = "des-from-db-all-employee"
DES_FROM_DB_DETAIL_EMPLOYEE = "des-from-db-detail-employee"
DES_FOR_ADD_EMPLOYEE = "des-for-add-employee"
DES_FOR_EDIT_EMPLOYEE = "des-for-edit-employee"


class EmployeeDeserializer(BaseDeserializer):

    @classmethod
    def _get_deserializer(cls, format_des: str):
        if format_des == DES_FROM_DB_ALL_EMPLOYEE:
            return cls._des_from_db_all_employee
        elif format_des == DES_FOR_ADD_EMPLOYEE:
            return cls._des_for_add_employee
        elif format_des == DES_FOR_EDIT_EMPLOYEE:
            return cls._des_for_edit_employee
        elif format_des == DES_FROM_DB_DETAIL_EMPLOYEE:
            return cls._des_from_db_detail_employee
        else:
            raise TypeError

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

    @staticmethod
    def _des_for_add_employee(req_form):
        return Employee(
            login=req_form.get('login'),
            name=req_form.get('name'),
            surname=req_form.get('surname'),
            specialty=req_form.get('specialty'),
        )

    @staticmethod
    def _des_for_edit_employee(req_form):
        return Employee(
            login=req_form.get('login') if req_form.get('login') else '-1',
            name=req_form.get('name') if req_form.get('name') else '-1',
            surname=req_form.get('surname') if req_form.get('surname') else '-1',
            specialty=req_form.get('specialty') if req_form.get('specialty') else '-1'
        )

    @staticmethod
    def _des_from_db_detail_employee(row):
        return Employee(
            id=row.get('employee_id'),
            login=row.get('employee_login'),
            name=row.get('employee_name'),
            surname=row.get('employee_surname'),
            specialty=row.get('employee_specialty'),
        )
