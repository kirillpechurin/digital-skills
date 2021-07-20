from portfolio.drivers.mail_server import MailServer, EMAIL_ACCEPT_REQUEST
from portfolio.internal.biz.dao.request_to_organisation import RequestToOrganisationDao
from portfolio.models.request_to_organisation import RequestToOrganisation


class RequestToOrganisationService:

    @staticmethod
    def make_request(request_to_organisation: RequestToOrganisation):
        request_to_organisation, err = RequestToOrganisationDao().add(request_to_organisation)
        if err:
            return None, err
        return request_to_organisation, None

    @staticmethod
    def get_all_requests_by_org_id(request_to_organisation: RequestToOrganisation):
        list_request_to_organisation, err = RequestToOrganisationDao().get_all_by_org_id(request_to_organisation)
        if err:
            return None, err

        return list_request_to_organisation, None

    @staticmethod
    def get_request_by_org_id(request_to_organisation: RequestToOrganisation):
        request_to_organisation, err = RequestToOrganisationDao().get_by_id(request_to_organisation.id)
        if err:
            return None, err
        return request_to_organisation, None

    @staticmethod
    def delete_request(request_to_organisation: RequestToOrganisation):
        request_to_organisation, err = RequestToOrganisationDao().remove_by_id(request_to_organisation.id)
        if err:
            return None, err
        return request_to_organisation, None

    @staticmethod
    def accept_request(request_to_organisation: RequestToOrganisation):
        request_to_organisation, err = RequestToOrganisationDao().accept_request(request_to_organisation)
        if err:
            return None, err

        request_to_organisation.parents.account_main.is_email_sent = MailServer.send_email(
            EMAIL_ACCEPT_REQUEST,
            request_to_organisation.parents.account_main.email,
            request_to_organisation.status)

        return request_to_organisation, None
