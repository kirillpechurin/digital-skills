from configs.settings import MAIL_FROM, MAIL_HOST, MAIL_PORT, MAIL_PASSWORD

import yagmail

EMAIL_CODE_TYPE = 'email_code_type'
EMAIL_RECOVERY_PASSWORD_TYPE = 'email_recovery_password_type'
EMAIL_ACCEPT_REQUEST = 'email_accept_request'


class MailServer:

    @classmethod
    def send_email(cls, message_type: str, address: str, message: str):
        sender = cls._get_sender(message_type)
        return sender(cls, address, message)

    @classmethod
    def _get_sender(cls, message_type: str):
        if message_type == EMAIL_CODE_TYPE:
            return cls._email_code_sender
        elif message_type == EMAIL_RECOVERY_PASSWORD_TYPE:
            return cls._email_temp_psw_sender
        elif message_type == EMAIL_ACCEPT_REQUEST:
            return cls._email_accept_request
        else:
            raise TypeError

    @classmethod
    def _get_connection(cls):
        yagmail.register(MAIL_FROM, MAIL_PASSWORD)
        return yagmail.SMTP(
            user=MAIL_FROM,
        )

    @staticmethod
    def _email_code_sender(cls, address: str, message: str) -> bool:
        yag = cls._get_connection()

        to = address
        body = message
        subject = "Код подтверждения для Portfolio"
        try:
            yag.send(to=to,
                     subject=subject,
                     contents=[body])
            print('i sended')
        except:
            print('[x] Unsuccessfully sent email to %s' % address)
            return False
        else:
            print('[i] Successfully sent email to %s' % address)
            return True
        finally:
            print("final")

    @staticmethod
    def _email_temp_psw_sender(cls, address: str, message: str) -> bool:
        yag = cls._get_connection()

        to = address
        body = message
        subject = "Временный пароль"

        try:
            yag.send(to=to,
                     subject=subject,
                     contents=[body])
            print('i sended')
        except:
            print('[x] Unsuccessfully sent email to %s' % address)
            return False
        else:
            print('[i] Successfully sent email to %s' % address)
            return True
        finally:
            print("final")

    @staticmethod
    def _email_accept_request(cls, address: str, message: str) -> bool:
        yag = cls._get_connection()

        to = address
        body = f'Статус вашей заявки: {message}'
        subject = "Статус заявки Portfolio"

        try:
            yag.send(to=to,
                     subject=subject,
                     contents=[body])
            print('i sended')
        except:
            print('[x] Unsuccessfully sent email to %s' % address)
            return False
        else:
            print('[i] Successfully sent email to %s' % address)
            return True
        finally:
            print("final")
