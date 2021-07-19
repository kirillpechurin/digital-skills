from portfolio.internal.biz.dao.employee import EmployeeDao
from portfolio.models.employee import Employee


class EmployeeService:
    @staticmethod
    def get_list_employee_by_org_id(organisation_id: int):
        list_teacher, err = EmployeeDao().get_list_employee_by_org_id(organisation_id)
        if err:
            return None, err
        return list_teacher, None

    @staticmethod
    def add_employee(employee: Employee):
        employee, err = EmployeeDao().add(employee)
        if err:
            return None, err

        return employee, None

    @staticmethod
    def update_employee(employee: Employee):
        teacher, err = EmployeeDao().update(employee.id, employee)
        if err:
            return None, err
        return teacher, None

    @staticmethod
    def delete_employee(employee: Employee):
        employee, err = EmployeeDao().remove_by_id(employee.id)
        if err:
            return None, err
        return employee, None
