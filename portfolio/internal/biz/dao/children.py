import psycopg2
import sqlalchemy
from sqlalchemy import insert

from portfolio.internal.biz.dao.base_dao import BaseDao
from portfolio.internal.biz.deserializers.children import ChildrenDeserialize, DES_FROM_DB_INFO_CHILDREN, \
    DES_FROM_DB_INFO_CHILD
from portfolio.models.children import Children
from portfolio.models.parents import Parents


class ChildrenDao(BaseDao):

    def add(self, children: Children):
        sql = insert(
            Children
        ).values(
            parents_id=children.parents.id,
            name=children.name,
            surname=children.surname,
            date_born=children.date_born,
        ).returning(
            Children._id.label('children_id'),
            Children._created_at.label('children_created_at'),
            Children._edited_at.label('children_edited_at'),
        )
        with self.session() as sess:
            try:
                row = sess.execute(sql).first()
                sess.commit()
            except sqlalchemy.exc.IntegrityError as exception:
                if str(exception.orig)[48:48+len("unique_children")] == 'unique_children':
                    return None, "Ребенок уже добавлен"
                else:
                    raise exception
        row = dict(row)
        children.id = row['children_id']
        children.created_at = row['children_created_at']
        children.edited_at = row['children_edited_at']
        return children, None

    def get_all_by_parents_id(self, children: Children):
        with self.session() as sess:
            data = sess.query(
                Children._id.label('children_id'),
                Children._name.label('children_name'),
                Children._surname.label('children_surname'),
                Children._date_born.label('children_date_born'),
                Children._parents_id.label('children_parents_id')
            ).join(
                Children._parents
            ).where(Parents._id == children.parents.id).all()
        if not data:
            return None, None
        data = [dict(row) for row in data]
        return ChildrenDeserialize.deserialize(data, DES_FROM_DB_INFO_CHILDREN), None

    def get_by_id(self, children_id: int):
        with self.session() as sess:
            row = sess.query(
                Children._id.label('children_id'),
                Children._name.label('children_name'),
                Children._surname.label('children_surname'),
                Children._date_born.label('children_date_born')
            ).where(Children._id == children_id).first()
        if not row:
            return None, "Сначала добавьте ребенка"
        row = dict(row)
        return ChildrenDeserialize.deserialize(row, DES_FROM_DB_INFO_CHILD), None

    def update(self, children_id: int, children: Children):
        with self.session() as sess:
            children_db = sess.query(Children).where(Children._id == children_id).first()
            for column in children_db:
                if not getattr(children, f"{column}") == '-1':
                    children_db[f'{column}'] = getattr(children, f"{column}")
            sess.commit()
        return children
