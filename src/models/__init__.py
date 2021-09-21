import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

_DB_URI = "sqlite:///database.db"
BASE = declarative_base()

from .equipment import Equipment
from .equipmentchecks import EquipmentChecks
from .member import Member
from .psa import Psa

ENGINE = sqlalchemy.create_engine(_DB_URI)

BASE.metadata.create_all(ENGINE)
DBSession = sqlalchemy.orm.sessionmaker(bind=ENGINE)
session = DBSession()
