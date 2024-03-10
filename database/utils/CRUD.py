from typing import Dict, List, TypeVar
from database.common.models import ModelBase, db
from peewee import ModelSelect


T = TypeVar('T')


def _store_data(db: db, model: T, *data: List[Dict]) -> None:
    """Function for storing data in the database"""
    with db.atomic():
        model.insert_many(*data).execute()


def _retrieve_all_data(db: db, user: str, model: T, *columns: ModelBase) -> ModelSelect:
    """Function for retrieving data from the database"""
    with db.atomic():
        response = model.select(*columns).where(model.user == user)

    return response


class CRUDInterface:
    """Interface for manipulating with the database"""
    @staticmethod
    def create():
        return _store_data

    @staticmethod
    def retrieve():
        return _retrieve_all_data


if __name__ == '__main__':
    _store_data()
    _retrieve_all_data()
    CRUDInterface()
