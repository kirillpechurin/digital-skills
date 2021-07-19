from portfolio.internal.biz.dao.request_to_organisation import RequestToOrganisationDao
from portfolio.models.request_to_organisation import RequestToOrganisation


class RequestToOrganisationService:

    @staticmethod
    def make_request(request_to_organisation: RequestToOrganisation):
        request_to_organisation, err = RequestToOrganisationDao().add(request_to_organisation)
        if err:
            return None, err
        return request_to_organisation, None
