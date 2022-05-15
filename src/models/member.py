import sqlalchemy

from . import BASE


class Member(BASE):
    __tablename__ = "member"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    lastname = sqlalchemy.Column(sqlalchemy.String)
    firstname = sqlalchemy.Column(sqlalchemy.String)

    dateCreated = sqlalchemy.Column(sqlalchemy.Date)
    dateEdited = sqlalchemy.Column(sqlalchemy.Date)
    deleted = sqlalchemy.Column(sqlalchemy.Boolean)

    psa = sqlalchemy.orm.relationship("Psa", uselist=False, backref="member")
