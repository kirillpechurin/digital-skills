from sqlalchemy import insert

from portfolio.internal.biz.dao.base_dao import BaseDao
from portfolio.models.account_main import AccountMain
from portfolio.models.account_session import AccountSession


class AccountSessionDao(BaseDao):

    def add(self, account_session: AccountSession):
        sql = insert(
            AccountSession
        ).values(
            account_main_id=account_session.account_main.id
        ).returning(
            AccountSession._id.label('account_session_id')
        )
        with self.session() as sess:
            row = sess.execute(sql).first()
            sess.commit()
        print(row)
        if not row:
            return None, None
        account_session.id = row['account_session_id']
        return account_session, None

    def get_by_session_id(self, session_id: int):
        with self.session() as sess:
            row = sess.query(
                AccountSession._account_main_id.label("account_session_account_main_id")
            ).where(
                AccountSession._id == session_id
            ).first()
        if not row:
            return None, None
        print(row)
        return AccountSession(id=row['account_session_account_main_id']), None

    def get_by_session_id_with_confirmed(self, session_id: int):
        with self.session() as sess:
            row = sess.query(
                AccountSession._account_main_id.label('account_session_account_main_id'),
                AccountMain._is_confirmed.label('account_main_is_confirmed')
            ).join(AccountSession._account_main).where(AccountSession._id == session_id).first()
            if not row:
                return None, None
        return AccountMain(
            id=row['account_session_account_main_id'],
            is_confirmed=row['account_main_is_confirmed']
        ), None
