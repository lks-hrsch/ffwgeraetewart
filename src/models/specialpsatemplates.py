import sqlalchemy

from . import BASE


class SpecialPsaTemplates(BASE):
    __tablename__ = "specialpsatemplates"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    type = sqlalchemy.Column(sqlalchemy.String)
    templatePath = sqlalchemy.Column(sqlalchemy.String)
    propertyKeys = sqlalchemy.Column(sqlalchemy.String)

    dateCreated = sqlalchemy.Column(sqlalchemy.Date)
    dateEdited = sqlalchemy.Column(sqlalchemy.Date)
    deleted = sqlalchemy.Column(sqlalchemy.Boolean)
