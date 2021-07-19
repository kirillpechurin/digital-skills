from portfolio.internal.biz.dao.organisation import OrganisationDao


class OrganisationService:

    @staticmethod
    def get_all_organisations():
        list_organisations, err = OrganisationDao().get_all()
        if err:
            return None, err
        return list_organisations, None

    @staticmethod
    def get_by_id(organisation_id: int):
        organisation, err = OrganisationDao().get_by_id(organisation_id)
        if err:
            return None, err
        return organisation, None
