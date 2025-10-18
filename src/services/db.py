from sqlalchemy import inspect
from sqlalchemy.orm.exc import MultipleResultsFound

from src.db import DBConnSingleton, Base


def create_or_get(obj: Base) -> Base:
    attrs_to_drop = ['id']
    attr_vals = {
        attr.key: getattr(obj, attr.key)
        for attr in inspect(obj).mapper.column_attrs
        if not attr.key in attrs_to_drop}
    with DBConnSingleton().get_session() as s:
        try:
            res = s.query(type(obj)).filter_by(**attr_vals).one_or_none()
        except MultipleResultsFound:
            raise MultipleResultsFound(f'Multiple findings for {type(obj)} with params {attr_vals} found.')

    if res is None:
        s.add(obj)
        s.commit()
        return s.merge(obj)
    else: return res

