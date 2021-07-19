from load_env import LIFETIME_CODE
from portfolio.drivers.mail_server import MailServer, EMAIL_CODE_TYPE
from portfolio.internal.biz.dao.account_main import AccountMainDao
from portfolio.internal.biz.dao.account_session import AccountSessionDao
from portfolio.internal.biz.dao.auth_code import AuthCodeDao
from portfolio.internal.biz.dao.organisation import OrganisationDao
from portfolio.internal.biz.dao.parents import ParentsDao
from portfolio.internal.biz.services.utils import get_passed_time
from portfolio.models.account_main import AccountMain
from portfolio.models.account_session import AccountSession
from portfolio.models.auth_code import AuthCode


class AuthService:

    @staticmethod
    def register(account_main: AccountMain, organisation, parent):
        account_main.create_hash_password()
        account_main.is_confirmed = False
        account_main, errors = AuthService._add_account_main_and_create_session(account_main, organisation, parent)
        if errors:
            return None, errors

        auth_code = AuthCode(account_main=account_main)
        auth_code.create_random_code()

        _, errors = AuthCodeDao().add(auth_code)
        if errors:
            return None, errors

        account_main.is_email_sent = MailServer.send_email(EMAIL_CODE_TYPE, account_main.email, auth_code.code)

        return account_main, None

    @staticmethod
    def _add_account_main_and_create_session(account_main: AccountMain, organisation, parent):
        account_main, errors = AccountMainDao().add(account_main)
        if errors:
            return None, errors

        account_main, errors = AuthService.create_by_role_account(account_main, organisation, parent)
        if errors:
            return None, errors

        account_main, errors = AuthService._create_session(account_main)
        if errors:
            return None, errors

        return account_main, None

    @staticmethod
    def create_by_role_account(account_main: AccountMain, organisation, parent):
        if account_main.account_role.id == 1:  # Organisation
            organisation, err = OrganisationDao().add_by_register(organisation)
            if err:
                return None, err
        elif account_main.account_role.id == 2:  # Parent
            parent, err = ParentsDao().add_by_register(parent)
            if err:
                return None, err
        return account_main, None

    @staticmethod
    def _create_session(account_main: AccountMain):
        account_session = AccountSession(account_main=account_main)
        account_session, err = AccountSessionDao().add(account_session)
        if err:
            return None, err

        account_main.auth_token = account_session.create_token()

        return account_main, None

    @staticmethod
    def confirm_code(auth_code: AuthCode):
        auth_code, err = AuthCodeDao().get_code_by_account_main_id(auth_code)
        if err:
            return None, err

        if not auth_code:
            return None, "Указан неизвестный код подтверждения"

        # if get_passed_time(auth_code.edited_at) > LIFETIME_CODE:
        #     return None, "Код недействителен"

        _, err = AuthCodeDao().set_is_confirm(auth_code.account_main.id, True)
        if err:
            return None, "Ошибочка"

        _, err = AuthCodeDao().remove_by_id(auth_code.id)
        if err:
            return None, "Не удалилось"

        return None, None

    @staticmethod
    def get_account_main_by_session_id(session_id: int):
        account_main, err = AccountSessionDao().get_by_session_id(session_id)
        if err:
            return None, err

        return account_main, None

    @staticmethod
    def get_account_main_by_session_id_with_confirmed(session_id: int):
        account_main, err = AccountSessionDao().get_by_session_id_with_confirmed(session_id)
        if err:
            return None, err

        return account_main, None

    @staticmethod
    def auth_login(account_main: AccountMain):
        account_main.create_hash_password()
        account_main, err = AccountMainDao().get_by_email_and_hash_password(account_main)
        if err:
            return None, err

        if not account_main:
            return None, "Неверный email"

        account_session = AccountSession(account_main=account_main)
        account_session, err = AccountSessionDao().add(account_session)
        if err:
            return None, err

        account_main.auth_token = account_session.create_token()

        return account_main, None

    @staticmethod
    def update_password(old_password: str, account_main_new: AccountMain):
        account_main_with_old_password = AccountMain(password=old_password)
        account_main_with_old_password.create_hash_password()

        account_main, err = AccountMainDao().get_by_id(account_main_new.id)
        if err:
            return None, err

        if account_main.hash_password != account_main_with_old_password.hash_password:
            return None, "Пароли неверны, попробуйте еще раз"

        account_main_new.create_hash_password()
        account_main, err = AccountMainDao().update_password(account_main.id, account_main_new)
        if err:
            return None, err
        return account_main, None
