import sqlalchemy
from sqlalchemy import orm

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

    @staticmethod
    def get_by_id(id: str, session):
        return session.query(Member).filter(Member.id.is_(id)).filter(Member.deleted.is_(False)).one()

    @staticmethod
    def get_next_id(session) -> int:
        current_highest_id_member: Member = session.query(Member).order_by(Member.id.desc()).first()
        return (
            int(current_highest_id_member.id) + 1
            if current_highest_id_member
            else 100
        )

    @staticmethod
    def get_all(session):
        return session.query(Member).filter(Member.deleted.is_(False)).order_by(Member.lastname).all()
