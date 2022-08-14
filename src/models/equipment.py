import sqlalchemy
from sqlalchemy import orm

from . import BASE


class Equipment(BASE):
    __tablename__ = "equipment"

    id = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    category = sqlalchemy.Column(sqlalchemy.String)
    vendor = sqlalchemy.Column(sqlalchemy.String)
    year = sqlalchemy.Column(sqlalchemy.String)

    dateCreated = sqlalchemy.Column(sqlalchemy.Date)
    dateEdited = sqlalchemy.Column(sqlalchemy.Date)
    deleted = sqlalchemy.Column(sqlalchemy.Boolean)

    checks = sqlalchemy.orm.relationship("EquipmentChecks", backref="equipment")

    @staticmethod
    def get_by_id(id: str, session):
        return session.query(Equipment).filter(Equipment.id.is_(id)).filter(Equipment.deleted.is_(False)).one()

    @staticmethod
    def get_all(session):
        return session.query(Equipment).filter(Equipment.deleted.is_(False)).order_by(Equipment.id).all()
