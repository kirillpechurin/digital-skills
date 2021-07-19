from sqlalchemy import insert

from portfolio.internal.biz.dao.base_dao import BaseDao
from portfolio.internal.biz.deserializers.organisation import OrganisationDeserializer, DES_FROM_DB_ALL_ORGANISATIONS, \
    DES_FROM_DB_DETAIL_ORGANISATION
from portfolio.models.organisation import Organisation


class OrganisationDao(BaseDao):

    def add_by_register(self, organisation: Organisation):
        sql = insert(
            Organisation
        ).values(
            account_main_id=organisation.account_main.id,
            name=organisation.name,
            login=organisation.login,
            photo_link=organisation.photo_link,
            description=organisation.description
        ).returning(
            Organisation._id.label('organisation_id'),
            Organisation._created_at.label('organisation_created_at'),
            Organisation._edited_at.label('organisation_edited_at')
        )
        with self.session() as sess:
            row = sess.execute(sql).first()
            sess.commit()
        print(row)
        if not row:
            return None, None
        organisation.id = row['organisation_id']
        organisation.created_at = row['organisation_created_at']
        organisation.edited_at = row['organisation_edited_at']
        return organisation, None

    def get_all(self):
        with self.session() as sess:
            data = sess.query(
                Organisation._id.label('organisation_id'),
                Organisation._name.label('organisation_name'),
                Organisation._login.label('organisation_login'),
                Organisation._photo_link.label('organisation_photo_link'),
                Organisation._description.label('organisation_description'),
            ).all()
        if not data:
            return None, None
        return OrganisationDeserializer.deserialize(data, DES_FROM_DB_ALL_ORGANISATIONS), None

    def get_by_id(self, organisation_id: int):
        with self.session() as sess:
            row = sess.query(
                Organisation._id.label('organisation_id'),
                Organisation._name.label('organisation_name'),
                Organisation._login.label('organisation_login'),
                Organisation._photo_link.label('organisation_photo_link'),
                Organisation._description.label('organisation_description'),
            ).where(Organisation._id == organisation_id).first()
        if not row:
            return None, None
        return OrganisationDeserializer.deserialize(row, DES_FROM_DB_DETAIL_ORGANISATION), None
