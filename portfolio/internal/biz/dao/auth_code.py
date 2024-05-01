from sqlalchemy import insert, delete

from enums.error.errors_enum import ErrorEnum
from internal.biz.dao.base_dao import BaseDao
from models.account_main import AccountMain
from models.auth_code import AuthCode


class AuthCodeDao(BaseDao):

    def add(self, auth_code: AuthCode):
        sql = insert(
            AuthCode
        ).values(
            account_main_id=auth_code.account_main.id,
            code=auth_code.code
        ).returning(
            AuthCode._id.label('auth_code_id'),
            AuthCode._created_at.label('auth_code_created_at'),
            AuthCode._edited_at.label('auth_code_edited_at'),
        )
        with self.session() as sess:
            row = sess.execute(sql).first()
            sess.commit()
        row = dict(row)
        auth_code.id = row['auth_code_id']
        auth_code.created_at = row['auth_code_created_at']
        auth_code.edited_at = row['auth_code_edited_at']
        return auth_code, None

    def get_code_by_account_main_id(self, auth_code: AuthCode):
        with self.session() as sess:
            row = sess.query(
                AuthCode._id.label("auth_code_id"),
                AuthCode._edited_at.label("auth_code_edited_at"),
                AuthCode._account_main_id.label('auth_code_account_main_id')
            ).where(AuthCode._code == auth_code.code).first()
        if not row:
            return None, ErrorEnum.auth_code_not_found
        row = dict(row)
        auth_code.id = row['auth_code_id']
        auth_code.edited_at = row['auth_code_edited_at']
        auth_code.account_main = AccountMain(id=row['auth_code_account_main_id'])
        return auth_code, None

    def set_is_confirm(self, account_main_id: int, is_confirmed: bool):
        with self.session() as sess:
            account_main = sess.query(AccountMain).where(AccountMain._id == account_main_id).first()
            if not account_main:
                return None, ErrorEnum.account_not_found
            account_main._is_confirmed = is_confirmed
            sess.commit()
        return None, None

    def remove_by_id(self, auth_code_id: int):
        sql = delete(
            AuthCode
        ).where(AuthCode._id == auth_code_id)
        with self.session() as sess:
            sess.execute(sql)
            sess.commit()
        return None, None
