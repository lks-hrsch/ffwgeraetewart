import sqlalchemy
from sqlalchemy.sql.schema import ForeignKey

from . import BASE


class EquipmentChecks(BASE):
    __tablename__ = "equipmentchecks"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    eid = sqlalchemy.Column(sqlalchemy.Integer, ForeignKey("equipment.id"))
    test_date = sqlalchemy.Column(sqlalchemy.String)
    remark = sqlalchemy.Column(sqlalchemy.String)
    testVision = sqlalchemy.Column(sqlalchemy.String)
    testFunction = sqlalchemy.Column(sqlalchemy.String)
    tester = sqlalchemy.Column(sqlalchemy.String)

    dateCreated = sqlalchemy.Column(sqlalchemy.Date)
    dateEdited = sqlalchemy.Column(sqlalchemy.Date)
    deleted = sqlalchemy.Column(sqlalchemy.Boolean)
