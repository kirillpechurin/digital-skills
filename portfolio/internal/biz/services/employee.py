from portfolio.internal.biz.dao.employee import EmployeeDao


class EmployeeService:
    @staticmethod
    def get_list_employee_by_org_id(organisation_id: int):
        list_teacher, err = EmployeeDao().get_list_employee_by_org_id(organisation_id)
        if err:
            return None, err
        return list_teacher, None
