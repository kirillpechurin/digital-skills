import sqlalchemy
from sqlalchemy import insert

from enums.error.errors_enum import ErrorEnum
from internal.biz.dao.base_dao import BaseDao
from models.parents import Parents


class ParentsDao(BaseDao):

    def add_by_register(self, parent: Parents):
        sql = insert(
            Parents
        ).values(
            account_main_id=parent.account_main.id,
            name=parent.name,
            surname=parent.surname
        ).returning(
            Parents._id.label('parents_id'),
            Parents._created_at.label('parents_created_at'),
            Parents._edited_at.label('parents_edited_at'),
        )
        with self.session() as sess:
            try:
                row = sess.execute(sql).first()
                sess.commit()
            except sqlalchemy.exc.IntegrityError as exception:
                if str(exception.orig)[48:48 + len("unique_parents")] == 'unique_parents':
                    return None, ErrorEnum.parents_already_exists
                else:
                    raise TypeError
        row = dict(row)
        parent.id = row['parents_id']
        parent.created_at = row['parents_created_at']
        parent.edited_at = row['parents_edited_at']
        return parent, None

    def get_by_account_id(self, account_main_id: int):
        with self.session() as sess:
            row = sess.query(
                Parents._id.label('parents_id'),
                Parents._name.label('parents_name'),
                Parents._surname.label('parents_surname'),
            ).where(Parents._account_main_id == account_main_id).first()
        if not row:
            return None, ErrorEnum.parents_not_found
        row = dict(row)
        parents = Parents(
            id=row.get('parents_id'),
            name=row.get('parents_name'),
            surname=row.get('parents_surname')
        )
        return parents, None
