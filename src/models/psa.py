import sqlalchemy
from sqlalchemy.sql.schema import ForeignKey

from . import BASE


class Psa(BASE):
    __tablename__ = "psa"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    mid = sqlalchemy.Column(sqlalchemy.String(length=4), ForeignKey("member.id"))
    eJacke = sqlalchemy.Column(sqlalchemy.String)
    eHose = sqlalchemy.Column(sqlalchemy.String)
    aJacke = sqlalchemy.Column(sqlalchemy.String)
    aHose = sqlalchemy.Column(sqlalchemy.String)
    hNummer = sqlalchemy.Column(sqlalchemy.String)
    hDate = sqlalchemy.Column(sqlalchemy.String)
    sGloves = sqlalchemy.Column(sqlalchemy.String)
    sShoe = sqlalchemy.Column(sqlalchemy.String)
    kHaube = sqlalchemy.Column(sqlalchemy.String)

    dateCreated = sqlalchemy.Column(sqlalchemy.Date)
    dateEdited = sqlalchemy.Column(sqlalchemy.Date)
    deleted = sqlalchemy.Column(sqlalchemy.Boolean)
