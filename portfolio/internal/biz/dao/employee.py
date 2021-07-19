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
