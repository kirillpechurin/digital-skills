from sqlalchemy import insert, and_

from portfolio.internal.biz.dao.base_dao import BaseDao
from portfolio.internal.biz.deserializers.account_main import AccountMainDeserializer, DES_FROM_DB_ACCOUNT_MAIN_DETAIL
from portfolio.models.account_main import AccountMain
from portfolio.models.account_session import AccountSession

UNIQUE_ACCOUNT_EMAIL = "unique_account_email"

ACCOUNT_MAIN = "account_main"
ACCOUNT_MAIN_ID = ACCOUNT_MAIN + "_id"
ACCOUNT_MAIN_CREATED_AT = ACCOUNT_MAIN + "_created_at"
ACCOUNT_MAIN_EDITED_AT = ACCOUNT_MAIN + "_edited_at"
ACCOUNT_MAIN_EMAIL = ACCOUNT_MAIN + "_email"
ACCOUNT_MAIN_NAME = ACCOUNT_MAIN + "_name"
ACCOUNT_MAIN_HASH_PASSWORD = ACCOUNT_MAIN + "_hash_password"
ACCOUNT_MAIN_IS_CONFIRMED = ACCOUNT_MAIN + "_is_confirmed"
ACCOUNT_MAIN_ACCOUNT_ROLE_ID = ACCOUNT_MAIN + "_account_role_id"


class AccountMainDao(BaseDao):

    def add(self, account_main: AccountMain):
        stmt = insert(
            AccountMain
        ).values(
            email=account_main.email,
            name=account_main.name,
            hash_password=account_main.hash_password,
            is_confirmed=account_main.is_confirmed,
            account_role_id=account_main.account_role.id
        ).returning(
            AccountMain._id.label(ACCOUNT_MAIN_ID),
            AccountMain._created_at.label(ACCOUNT_MAIN_CREATED_AT),
            AccountMain._edited_at.label(ACCOUNT_MAIN_EDITED_AT)
        )
        with self.session() as sess:
            row = sess.execute(stmt).first()
            sess.commit()
        if not row:
            return None, None
        row = dict(row)
        account_main.id = row[ACCOUNT_MAIN_ID]
        account_main.created_at = row[ACCOUNT_MAIN_CREATED_AT]
        account_main.edited_at = row[ACCOUNT_MAIN_EDITED_AT]

        return account_main, None

    def get_by_id(self, account_main_id: int):
        with self.session() as sess:
            row = sess.query(
                AccountMain._id.label(ACCOUNT_MAIN_ID),
                AccountMain._created_at.label(ACCOUNT_MAIN_CREATED_AT),
                AccountMain._edited_at.label(ACCOUNT_MAIN_EDITED_AT),
                AccountMain._email.label(ACCOUNT_MAIN_EMAIL),
                AccountMain._name.label(ACCOUNT_MAIN_NAME),
                AccountMain._hash_password.label(ACCOUNT_MAIN_HASH_PASSWORD),
                AccountMain._is_confirmed.label(ACCOUNT_MAIN_IS_CONFIRMED),
                AccountMain._account_role_id.label(ACCOUNT_MAIN_ACCOUNT_ROLE_ID)
            ).where(AccountMain._id == account_main_id).first()
        if not row:
            return None, None
        row = dict(row)
        return AccountMainDeserializer.deserialize(row, DES_FROM_DB_ACCOUNT_MAIN_DETAIL), None

    def get_by_email_and_hash_password(self, account_main: AccountMain):
        with self.session() as sess:
            row = sess.query(
                AccountMain._id.label(ACCOUNT_MAIN_ID),
                AccountMain._created_at.label(ACCOUNT_MAIN_CREATED_AT),
                AccountMain._edited_at.label(ACCOUNT_MAIN_EDITED_AT),
                AccountMain._email.label(ACCOUNT_MAIN_EMAIL),
                AccountMain._name.label(ACCOUNT_MAIN_NAME),
                AccountMain._hash_password.label(ACCOUNT_MAIN_HASH_PASSWORD),
                AccountMain._is_confirmed.label(ACCOUNT_MAIN_IS_CONFIRMED),
                AccountMain._account_role_id.label(ACCOUNT_MAIN_ACCOUNT_ROLE_ID)
            ).where(and_(AccountMain._hash_password == account_main.hash_password, AccountMain._email == account_main.email)).first()
        if not row:
            return None, None
        row = dict(row)
        return AccountMainDeserializer.deserialize(row, DES_FROM_DB_ACCOUNT_MAIN_DETAIL), None

    def update_password(self, account_main_id: int, account_main: AccountMain):
        with self.session() as sess:
            account_main_db = sess.query(AccountMain).where(AccountMain._id == account_main_id).first()
            if not account_main_db:
                return None, None
            account_main_db._hash_password = account_main.hash_password
            sess.commit()
        return account_main, None
