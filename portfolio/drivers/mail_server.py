from portfolio.configs.mail_server import MAIL_FROM, MAIL_HOST, MAIL_PORT, MAIL_PASSWORD

import yagmail

EMAIL_CODE_TYPE = 'email_code_type'
EMAIL_RECOVERY_PASSWORD_TYPE = 'email_recovery_password_type'
EMAIL_ACCEPT_REQUEST = 'email_accept_request'


class MailServer:

    @classmethod
    def send_email(cls, message_type: str, address: str, message: str):
        sender = cls._get_sender(message_type)
        return sender(address, message)

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

    @staticmethod
    def _email_code_sender(address: str, message: str) -> bool:

        yagmail.register(MAIL_FROM, MAIL_PASSWORD)

        yag = yagmail.SMTP(MAIL_FROM)

        to = address
        body = message
        subject = "Код подтверждения для Portfolio"
        print(address)
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
    def _email_temp_psw_sender(address: str, message: str) -> bool:
        yagmail.register(MAIL_FROM, MAIL_PASSWORD)

        yag = yagmail.SMTP(MAIL_FROM)

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
    def _email_accept_request(address: str, message: str) -> bool:
        yagmail.register(MAIL_FROM, MAIL_PASSWORD)

        yag = yagmail.SMTP(MAIL_FROM)

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
