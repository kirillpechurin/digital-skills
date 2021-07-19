from sqlalchemy import insert

from portfolio.internal.biz.dao.base_dao import BaseDao
from portfolio.models.request_to_organisation import RequestToOrganisation


class RequestToOrganisationDao(BaseDao):

    def add(self, request_to_organisation: RequestToOrganisation):
        sql = insert(
            RequestToOrganisation
        ).values(
            parents_id=request_to_organisation.parents.id,
            events_id=request_to_organisation.events.id,
            children_id=request_to_organisation.children.id,
        ).returning(
            RequestToOrganisation._id.label('request_to_organisation_id'),
            RequestToOrganisation._created_at.label('request_to_organisation_created_at'),
            RequestToOrganisation._edited_at.label('request_to_organisation_edited_at')
        )
        with self.session() as sess:
            row = sess.execute(sql).first()
        if not row:
            return None, "Не успешно"
        request_to_organisation.id = row['request_to_organisation_id']
        request_to_organisation.created_at = row['request_to_organisation_created_at']
        request_to_organisation.edited_at = row['request_to_organisation_edited_at']
        return request_to_organisation, None
