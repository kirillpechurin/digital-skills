from portfolio.internal.biz.dao.base_dao import BaseDao
from portfolio.internal.biz.deserializers.account_role import AccountRoleDeserializer, SER_FOR_GET_LIST_ACCOUNT_ROLE
from portfolio.models.account_role import AccountRole


class AccountRoleDao(BaseDao):

    def get_by_id(self, account_role_id: int):
        with self.session() as sess:
            row = sess.query(
                AccountRole._id.label("account_role_id"),
                AccountRole._name.label("account_role_name")
            ).where(AccountRole._id == account_role_id).first()
        print(row)
        if not row:
            return None, None
        return AccountRole(id=row['account_role_id'],
                           name=row['account_role_name']), None

    def get_all(self):
        with self.session() as sess:
            data = sess.query(
                AccountRole._id.label("account_role_id"),
                AccountRole._name.label("account_role_name")
            ).all()
        print(data)
        return AccountRoleDeserializer.deserialize(data, SER_FOR_GET_LIST_ACCOUNT_ROLE), None
