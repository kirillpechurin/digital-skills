import sqlalchemy
from sqlalchemy import insert, and_, delete

from enums.error.errors_enum import ErrorEnum
from internal.biz.dao.base_dao import BaseDao
from internal.biz.dao.children_organisation import ChildrenOrganisationDao
from internal.biz.dao.events import EventsDao
from internal.biz.dao.events_child import EventsChildDao
from internal.biz.deserializers.request_to_organisation import RequestToOrganisationDeserializer, \
    DES_FROM_DB_ALL_ACTIVE_REQUESTS, DES_FROM_DB_DETAIL_REQUEST
from models.account_main import AccountMain
from models.children import Children
from models.children_organisation import ChildrenOrganisation
from models.events import Events
from models.events_child import EventsChild
from models.organisation import Organisation
from models.parents import Parents
from models.request_to_organisation import RequestToOrganisation


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
            try:
                row = sess.execute(sql).first()
                sess.commit()
                row = dict(row)
            except sqlalchemy.exc.IntegrityError as exception:
                if str(exception.orig)[48:48 + len("unique_request")] == 'unique_request':
                    return None, ErrorEnum.request_to_organisation_already_exists
                else:
                    raise TypeError
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
                    RequestToOrganisation._status == False
                )
            ).all()
        if not data:
            return None, None
        data = [dict(row) for row in data]
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
                    RequestToOrganisation._status == False
                )
            ).first()
        if not row:
            return None, ErrorEnum.request_to_organisation_not_found
        row = dict(row)
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
        row = dict(row)
        return RequestToOrganisation(id=row['id']), None

    def get_ids_by_req_id(self, request_to_organisation):
        row = self.sess_transaction.query(
            RequestToOrganisation._events_id.label('request_to_organisation_events_id'),
            Events._organisation_id.label('events_organisation_id'),
            RequestToOrganisation._children_id.label('request_to_organisation_children_id'),
            RequestToOrganisation._parents_id.label('request_to_organisation_parents_id'),
            AccountMain._id.label('parents_account_main_id'),
            AccountMain._email.label('parents_account_main_email'),
        ).join(
            RequestToOrganisation._parents
        ).join(
            Parents._account_main
        ).join(
            RequestToOrganisation._events
        ).where(
            RequestToOrganisation._id == request_to_organisation.id
        ).first()
        row = dict(row)
        request_to_organisation.events = Events(id=row['request_to_organisation_events_id'],
                                                organisation=Organisation(id=row['events_organisation_id']))
        request_to_organisation.children = Children(id=row['request_to_organisation_children_id'])
        request_to_organisation.parents = Parents(
            id=row['request_to_organisation_parents_id'],
            account_main=AccountMain(
                id=row['parents_account_main_id'],
                email=row['parents_account_main_email']
            )
        )
        return request_to_organisation, None

    def update_status(self, request_to_organisation: RequestToOrganisation):
        sess = self.sess_transaction
        request_to_organisation_db = sess.query(RequestToOrganisation).where(RequestToOrganisation._id == request_to_organisation.id).first()
        if not request_to_organisation_db:
            return None, ErrorEnum.request_to_organisation_not_found
        request_to_organisation_db._status = request_to_organisation.status
        sess.commit()
        return request_to_organisation, None

    def accept_request(self, request_to_organisation: RequestToOrganisation):
        try:
            self.sess_transaction = self.session()
            request_to_organisation, err = RequestToOrganisationDao(sess_transaction=self.sess_transaction).get_ids_by_req_id(request_to_organisation)
            if err:
                return None, err
            children_organisation = ChildrenOrganisation(children=request_to_organisation.children,
                                                         organisation=request_to_organisation.events.organisation)

            children_organisation_get_or_create, err = ChildrenOrganisationDao(sess_transaction=self.sess_transaction).get_or_create(children_organisation)
            if err:
                return None, err
            children_organisation.id = children_organisation_get_or_create.id

            events_child = EventsChild(
                events=Events(
                    id=request_to_organisation.events.id
                ),
                children_organisation=ChildrenOrganisation(
                    id=children_organisation.id,
                )
            )
            events, err = EventsDao(sess_transaction=self.sess_transaction).get_by_id(request_to_organisation.events.id)
            if err:
                return None, err
            events_child.events = events

            events_child, err = EventsChildDao(sess_transaction=self.sess_transaction).add_by_request(events_child)
            if err:
                return None, err
            request_to_organisation.status = True
            request_to_organisation, err = RequestToOrganisationDao(sess_transaction=self.sess_transaction).update_status(request_to_organisation)
            if err:
                return None, err

            self.sess_transaction.commit()
            return request_to_organisation, None
        except Exception as exc:
            self.sess_transaction.rollback()
            return None, ErrorEnum.request_to_organisation_failed
        finally:
            self.sess_transaction.close()
