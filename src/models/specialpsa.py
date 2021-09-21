import sqlalchemy
from sqlalchemy.sql.schema import ForeignKey

from . import BASE


class SpecialPsa(BASE):
    __tablename__ = "specialpsa"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    type = sqlalchemy.Column(sqlalchemy.String, ForeignKey("specialpsatemplates.type"))
    number = sqlalchemy.Column(sqlalchemy.String)
    propertys = sqlalchemy.Column(sqlalchemy.JSON)

    dateCreated = sqlalchemy.Column(sqlalchemy.Date)
    dateEdited = sqlalchemy.Column(sqlalchemy.Date)
    deleted = sqlalchemy.Column(sqlalchemy.Boolean)
