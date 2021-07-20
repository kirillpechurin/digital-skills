from portfolio.internal.biz.dao.base_dao import BaseDao
from portfolio.internal.biz.deserializers.children import ChildrenDeserialize, DES_FROM_DB_INFO_CHILDREN, \
    DES_FROM_DB_INFO_CHILD
from portfolio.models.children import Children
from portfolio.models.parents import Parents


class ChildrenDao(BaseDao):

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
        return ChildrenDeserialize.deserialize(row, DES_FROM_DB_INFO_CHILD), None

    def update(self, children_id: int, children: Children):
        with self.session() as sess:
            children_db = sess.query(Children).where(Children._id == children_id).first()
            for column in children_db:
                if not getattr(children, f"{column}") == '-1':
                    children_db[f'{column}'] = getattr(children, f"{column}")
            sess.commit()
        return children
