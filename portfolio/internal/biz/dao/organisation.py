import sqlalchemy.exc
from sqlalchemy import insert

from portfolio.enums.error.errors_enum import ErrorEnum
from portfolio.internal.biz.dao.base_dao import BaseDao
from portfolio.internal.biz.deserializers.organisation import OrganisationDeserializer, DES_FROM_DB_ALL_ORGANISATIONS, \
    DES_FROM_DB_DETAIL_ORGANISATION
from portfolio.models.account_main import AccountMain
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
            try:
                row = sess.execute(sql).first()
                sess.commit()
                row = dict(row)
            except sqlalchemy.exc.IntegrityError as exception:
                if str(exception.orig)[48:48 + len("unique_organisation")] == 'unique_organisation':
                    return None, ErrorEnum.organisation_already_exists

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
        data = [dict(row) for row in data]
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
            return None, ErrorEnum.organisation_not_found
        row = dict(row)
        return OrganisationDeserializer.deserialize(row, DES_FROM_DB_DETAIL_ORGANISATION), None

    def get_by_account_id(self, account_main_id: int):
        with self.session() as sess:
            row = sess.query(
                Organisation._id.label('organisation_id'),
                Organisation._created_at.label('organisation_created_at'),
                Organisation._name.label('organisation_name'),
                Organisation._photo_link.label('organisation_photo_link'),
                Organisation._description.label('organisation_description'),
                Organisation._login.label('organisation_login'),
                Organisation._account_main_id.label('organisation_account_main_id'),
            ).where(
                Organisation._account_main_id == account_main_id
            ).first()
        if not row:
            return None, ErrorEnum.organisation_not_found
        row = dict(row)
        organisation = Organisation(
            id=row['organisation_id'],
            created_at=row['organisation_created_at'],
            name=row['organisation_name'],
            photo_link=row['organisation_photo_link'],
            description=row['organisation_description'],
            login=row['organisation_login'],
            account_main=AccountMain(id=row['organisation_account_main_id'])
        )
        return organisation, None
