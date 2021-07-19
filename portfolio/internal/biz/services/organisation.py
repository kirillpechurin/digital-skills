from portfolio.internal.biz.dao.organisation import OrganisationDao


class OrganisationService:

    @staticmethod
    def get_all_organisations():
        list_organisations, err = OrganisationDao().get_all()
        if err:
            return None, err
        return list_organisations, None
