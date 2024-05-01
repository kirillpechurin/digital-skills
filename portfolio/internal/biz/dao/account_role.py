from typing import List

import sqlalchemy

from enums.error.errors_enum import ErrorEnum
from internal.biz.dao.base_dao import BaseDao
from internal.biz.deserializers.account_role import AccountRoleDeserializer, SER_FOR_GET_LIST_ACCOUNT_ROLE
from models.account_role import AccountRole


class AccountRoleDao(BaseDao):

    def get_by_id(self, account_role_id: int):
        with self.session() as sess:
            row = sess.query(
                AccountRole._id.label("account_role_id"),
                AccountRole._name.label("account_role_name")
            ).where(AccountRole._id == account_role_id).first()
        if not row:
            return None, ErrorEnum.account_role_not_found
        row = dict(row)
        return AccountRole(id=row['account_role_id'],
                           name=row['account_role_name']), None

    def get_all(self):
        with self.session() as sess:
            data = sess.query(
                AccountRole._id.label("account_role_id"),
                AccountRole._name.label("account_role_name")
            ).all()
        data = [dict(row) for row in data]
        return AccountRoleDeserializer.deserialize(data, SER_FOR_GET_LIST_ACCOUNT_ROLE), None

    def bulk_create(self, roles: List[AccountRole]):
        try:
            with self.session() as sess:
                for role in roles:
                    role._id = role.id
                    role._name = role.name
                    sess.add(role)
                sess.commit()
        except sqlalchemy.exc.IntegrityError as exception:
            if 'duplicate key value violates unique constraint "account_role_pkey"' in str(exception.orig):
                return None, None
            else:
                raise TypeError
