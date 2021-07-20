from typing import List

from portfolio.internal.biz.dao.children_organisation import ChildrenOrganisationDao
from portfolio.models.children import Children
from portfolio.models.children_organisation import ChildrenOrganisation


class ChildrenOrganisationService:

    @staticmethod
    def get_list_organisation_by_children_id(children_organisation: ChildrenOrganisation):
        list_org, err = ChildrenOrganisationDao().get_by_children_id(children_organisation.children.id)
        if err:
            return None, err
        return list_org, None

    @staticmethod
    def get_list_children_by_org_id(organisation_id: int):
        list_learners, err = ChildrenOrganisationDao().get_children_by_organisation_id(organisation_id)
        if err:
            return None, err
        return list_learners, None

    @staticmethod
    def get_children_by_children_org_id(children_organisation: ChildrenOrganisation):
        children_org, err = ChildrenOrganisationDao().get_children_by_children_org_id(children_organisation.id)
        if err:
            return None, err
        return children_org, None