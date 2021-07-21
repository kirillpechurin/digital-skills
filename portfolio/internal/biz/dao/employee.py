from datetime import datetime

from sqlalchemy import insert, delete

from portfolio.enums.error.errors_enum import ErrorEnum
from portfolio.internal.biz.dao.base_dao import BaseDao
from portfolio.internal.biz.deserializers.employee import EmployeeDeserializer, DES_FROM_DB_ALL_EMPLOYEE, \
    DES_FROM_DB_DETAIL_EMPLOYEE
from portfolio.models.employee import Employee


class EmployeeDao(BaseDao):

    def get_list_employee_by_org_id(self, organisation_id: int):
        with self.session() as sess:
            data = sess.query(
                Employee._id.label('employee_id'),
                Employee._login.label('employee_login'),
                Employee._name.label('employee_name'),
                Employee._surname.label('employee_surname'),
                Employee._specialty.label('employee_specialty'),
            ).where(
                Employee._organisation_id == organisation_id
            ).all()
        if not data:
            return None, None
        data = [dict(row) for row in data]
        return EmployeeDeserializer.deserialize(data, DES_FROM_DB_ALL_EMPLOYEE), None

    def add(self, employee: Employee):
        sql = insert(
            Employee
        ).values(
            login=employee.login,
            name=employee.name,
            surname=employee.surname,
            organisation_id=employee.organisation.id,
            specialty=employee.specialty,
        ).returning(
            Employee._id.label('employee_id'),
            Employee._created_at.label('employee_created_at'),
            Employee._edited_at.label('employee_edited_at'),
        )
        with self.session() as sess:
            row = sess.execute(sql).first()
            sess.commit()
        row = dict(row)
        employee.id = row['employee_id']
        employee.created_at = row['employee_created_at']
        employee.edited_at = row['employee_edited_at']
        return employee, None

    def update(self, employee_id: int, employee: Employee):
        with self.session() as sess:
            employee_db = sess.query(Employee).where(Employee._id == employee_id).first()
            created_at = employee_db._created_at
            for column in employee_db.__dict__:
                if getattr(employee, f"{column[1:]}", '-1') != '-1':
                    setattr(employee_db, f"{column}", getattr(employee, f"{column[1:]}"))
            setattr(employee_db, '_edited_at', datetime.utcnow())
            setattr(employee_db, '_created_at', created_at)
            sess.commit()
        return employee, None

    def remove_by_id(self, employee_id: int):
        sql = delete(
            Employee
        ).where(Employee._id == employee_id)
        with self.session() as sess:
            sess.execute(sql)
            sess.commit()
        return employee_id, None

    def get_by_id(self, employee_id: int):
        with self.session() as sess:
            row = sess.query(
                Employee._id.label('employee_id'),
                Employee._login.label('employee_login'),
                Employee._name.label('employee_name'),
                Employee._surname.label('employee_surname'),
                Employee._specialty.label('employee_specialty'),
            ).where(
                Employee._id == employee_id
            ).first()
        if not row:
            return None, ErrorEnum.employee_not_found
        row = dict(row)
        return EmployeeDeserializer.deserialize(row, DES_FROM_DB_DETAIL_EMPLOYEE), None
