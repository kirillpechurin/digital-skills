from sqlalchemy import insert, delete

from portfolio.internal.biz.dao.base_dao import BaseDao
from portfolio.internal.biz.deserializers.employee import EmployeeDeserializer, DES_FROM_DB_ALL_EMPLOYEE
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
            ).where(Employee._organisation_id == organisation_id).all()
        if not data:
            return None, None
        return EmployeeDeserializer.deserialize(data, DES_FROM_DB_ALL_EMPLOYEE), None

    def add(self, employee: Employee):
        sql = insert(
            Employee
        ).values(
            Employee._login,
            Employee._name,
            Employee._surname,
            Employee._organisation_id,
            Employee._specialty,
        ).returning(
            Employee._id.label('employee_id'),
            Employee._created_at.label('employee_created_at'),
            Employee._edited_at.label('employee_edited_at'),
        )
        with self.session() as sess:
            row = sess.execute(sql).first()
            sess.commit()
        employee.id = row['id']
        employee.created_at = row['created_at']
        employee.edited_at = row['edited_at']
        return employee, None

    def update(self, employee_id: int, employee: Employee):
        with self.session() as sess:
            employee_db = sess.query(Employee).where(Employee._id == employee_id).first()
            for column in employee_db:
                if not getattr(employee, f"{column}") == '-1':
                    employee_db[f'{column}'] = getattr(employee, f"{column}")
            sess.commit()
        return employee

    def remove_by_id(self, employee_id: int):
        sql = delete(
            Employee
        ).where(Employee._id == employee_id)
        with self.session() as sess:
            sess.execute(sql)
            sess.commit()
        return employee_id, None
