from sqlalchemy import insert, and_

from portfolio.internal.biz.dao.base_dao import BaseDao
from portfolio.internal.biz.deserializers.children_organisation import ChildrenOrganisationDeserializer, \
    DES_FROM_DB_LIST_LEARNERS, DES_FROM_DB_GET_DETAIL_LEARNER
from portfolio.models.children import Children
from portfolio.models.children_organisation import ChildrenOrganisation
from portfolio.models.organisation import Organisation


class ChildrenOrganisationDao(BaseDao):

    def get_by_children_id(self, children_id: int):
        with self.session() as sess:
            data = sess.query(
                ChildrenOrganisation._id.label(''),
                Organisation._id.label(''),
                Organisation._name.label('')
            ).join(
                ChildrenOrganisation._organisation
            ).where(ChildrenOrganisation._children_id == children_id).all()
        if not data:
            return None, None
        return [
            Organisation(
                id=org.get('organisation_id'),
                name=org.get('organisation_name')
            )
            for org in data
        ], None

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

        row = sess.execute(sql).first()

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
            return None, 'get_by_org_and_child_id'
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
        return ChildrenOrganisationDeserializer.deserialize(row, DES_FROM_DB_GET_DETAIL_LEARNER), None
