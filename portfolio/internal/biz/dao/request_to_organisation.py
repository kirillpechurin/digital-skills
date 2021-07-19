from sqlalchemy import insert, and_, delete

from portfolio.internal.biz.dao.base_dao import BaseDao
from portfolio.internal.biz.deserializers.request_to_organisation import RequestToOrganisationDeserializer, \
    DES_FROM_DB_ALL_ACTIVE_REQUESTS, DES_FROM_DB_DETAIL_REQUEST
from portfolio.models.children import Children
from portfolio.models.events import Events
from portfolio.models.parents import Parents
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
            sess.commit()
        if not row:
            return None, "Не успешно"
        request_to_organisation.id = row['request_to_organisation_id']
        request_to_organisation.created_at = row['request_to_organisation_created_at']
        request_to_organisation.edited_at = row['request_to_organisation_edited_at']
        return request_to_organisation, None

    def get_all_by_org_id(self, request_to_organisation: RequestToOrganisation):
        with self.session() as sess:
            data = sess.query(
                RequestToOrganisation._id.label('request_to_organisation_id'),
                RequestToOrganisation._status.label('request_to_organisation_status'),
                Events._id.label('events_id'),
                Events._name.label('events_name'),
                Events._date_event.label('events_date_event'),
                Parents._id.label('parents_id'),
                Parents._name.label('parents_name'),
                Parents._surname.label('parents_surname'),
                Children._id.label('children_id'),
                Children._name.label('children_name'),
                Children._surname.label('children_surname'),
                Children._date_born.label('children_date_born'),
            ).join(
                RequestToOrganisation._events
            ).join(
                RequestToOrganisation._parents
            ).join(
                RequestToOrganisation._children
            ).where(
                and_(
                    Events._organisation_id == request_to_organisation.events.organisation.id,
                    RequestToOrganisation._status is False
                )
            )
        if not data:
            return None, None
        return RequestToOrganisationDeserializer.deserialize(data, DES_FROM_DB_ALL_ACTIVE_REQUESTS), None

    def get_by_id(self, request_id: int):
        with self.session() as sess:
            row = sess.query(
                RequestToOrganisation._id.label('request_to_organisation_id'),
                RequestToOrganisation._status.label('request_to_organisation_status'),
                Events._id.label('events_id'),
                Events._type.label('events_type'),
                Events._name.label('events_name'),
                Events._date_event.label('events_date_event'),
                Events._hours.label('events_hours'),
                Events._skill.label('events_skill'),
                Parents._id.label('parents_id'),
                Parents._name.label('parents_name'),
                Parents._surname.label('parents_surname'),
                Children._id.label('children_id'),
                Children._name.label('children_name'),
                Children._surname.label('children_surname'),
                Children._date_born.label('children_date_born'),
            ).join(
                RequestToOrganisation._events
            ).join(
                RequestToOrganisation._parents
            ).join(
                RequestToOrganisation._children
            ).where(
                and_(
                    RequestToOrganisation._id == request_id,
                    RequestToOrganisation._status is False
                )
            ).first()
        if not row:
            return None, None
        return RequestToOrganisationDeserializer.deserialize(row, DES_FROM_DB_DETAIL_REQUEST), None

    def remove_by_id(self, request_id: int):
        sql = delete(
            RequestToOrganisation
        ).where(
            RequestToOrganisation._id == request_id
        ).returning(
            RequestToOrganisation._id.label('request_to_organisation_id')
        )
        with self.session as sess:
            row = sess.execute(sql).first()
            sess.commit()
        return RequestToOrganisation(id=row['id']), None
