import sqlalchemy
from sqlalchemy import insert, and_

from enums.error.errors_enum import ErrorEnum
from internal.biz.dao.base_dao import BaseDao
from internal.biz.deserializers.children_organisation import ChildrenOrganisationDeserializer, \
    DES_FROM_DB_LIST_LEARNERS, DES_FROM_DB_GET_DETAIL_LEARNER
from models.children import Children
from models.children_organisation import ChildrenOrganisation
from models.organisation import Organisation


class ChildrenOrganisationDao(BaseDao):

    def get_by_children_id(self, children_id: int):
        with self.session() as sess:
            data = sess.query(
                ChildrenOrganisation._id.label('children_organisation_id'),
                Organisation._id.label('organisation_id'),
                Organisation._name.label('organisation_name')
            ).join(
                ChildrenOrganisation._organisation
            ).where(
                ChildrenOrganisation._children_id == children_id
            ).all()
        if not data:
            return None, None
        data = [dict(row) for row in data]
        return [
            Organisation(
                id=org.get('organisation_id'),
                name=org.get('organisation_name')
            )
            for org in data
        ], None

    def get_or_create(self, children_organisation: ChildrenOrganisation):
        sess = self.sess_transaction
        row = sess.query(
            ChildrenOrganisation._id.label('children_organisation_id'),
        ).where(
            and_(
                ChildrenOrganisation._organisation_id == children_organisation.organisation.id,
                ChildrenOrganisation._children_id == children_organisation.children.id
            )
        ).first()
        if row:
            row = dict(row)
            children_organisation.id = row['children_organisation_id']
            return children_organisation, None

        sql = insert(
            ChildrenOrganisation
        ).values(
            organisation_id=children_organisation.organisation.id,
            children_id=children_organisation.children.id
        ).returning(
            ChildrenOrganisation._id.label('children_organisation_id'),
            ChildrenOrganisation._created_at.label('children_organisation_created_at'),
            ChildrenOrganisation._edited_at.label('children_organisation_edited_at')
        )
        try:
            row = sess.execute(sql).first()
            sess.commit()
            row = dict(row)
        except sqlalchemy.exc.IntegrityError as exception:
            if str(exception.orig)[48:48 + len("unique_children_organisation")] == 'unique_children_organisation':
                return None, "ALREADY_EXISTS"
            else:
                raise exception
        children_organisation.id = row['children_organisation_id']
        children_organisation.created_at = row['children_organisation_created_at']
        children_organisation.edited_at = row['children_organisation_edited_at']
        return children_organisation, None

    def add(self, children_organisation: ChildrenOrganisation):
        sess = self.sess_transaction
        sql = insert(
            ChildrenOrganisation
        ).values(
            organisation_id=children_organisation.organisation.id,
            children_id=children_organisation.children.id
        ).returning(
            ChildrenOrganisation._id.label('children_organisation_id'),
            ChildrenOrganisation._created_at.label('children_organisation_created_at'),
            ChildrenOrganisation._edited_at.label('children_organisation_edited_at')
        )
        try:
            row = sess.execute(sql).first()
            sess.commit()
        except sqlalchemy.exc.IntegrityError as exception:
            if str(exception.orig)[48:48 + len("unique_children_organisation")] == 'unique_children_organisation':
                return None, ErrorEnum.children_organisation_already_exists
            else:
                raise exception
        row = dict(row)
        children_organisation.id = row['children_organisation_id']
        children_organisation.created_at = row['children_organisation_created_at']
        children_organisation.edited_at = row['children_organisation_edited_at']
        return children_organisation, None

    def get_by_org_and_child_id(self, children_organisation: ChildrenOrganisation):
        sess = self.sess_transaction
        row = sess.query(
            ChildrenOrganisation._id.label('children_organisation_id'),
        ).where(
            and_(
                ChildrenOrganisation._organisation_id == children_organisation.organisation.id,
                ChildrenOrganisation._children_id == children_organisation.children.id
            )
        ).first()
        if not row:
            return None, ErrorEnum.children_organisation_not_found
        row = dict(row)
        children_organisation.id = row['children_organisation_id']
        return children_organisation, None

    def get_children_by_organisation_id(self, organisation_id: int):
        with self.session() as sess:
            data = sess.query(
                ChildrenOrganisation._id.label('children_organisation_id'),
                Children._id.label('children_id'),
                Children._name.label('children_name'),
                Children._surname.label('children_surname'),
                Children._date_born.label('children_date_born'),
            ).join(
                ChildrenOrganisation._children
            ).where(
                ChildrenOrganisation._organisation_id == organisation_id
            ).all()
        if not data:
            return None, None
        data = [dict(row) for row in data]
        return ChildrenOrganisationDeserializer.deserialize(data, DES_FROM_DB_LIST_LEARNERS), None

    def get_children_by_children_org_id(self, children_organisation_id: int):
        with self.session() as sess:
            row = sess.query(
                ChildrenOrganisation._id.label('children_organisation_id'),
                Children._id.label('children_id'),
                Children._name.label('children_name'),
                Children._surname.label('children_surname'),
                Children._date_born.label('children_date_born')
            ).join(
                ChildrenOrganisation._children
            ).where(
                ChildrenOrganisation._id == children_organisation_id
            ).first()
        row = dict(row)
        if not row:
            return None, None
        return ChildrenOrganisationDeserializer.deserialize(row, DES_FROM_DB_GET_DETAIL_LEARNER), None
