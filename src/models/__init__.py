import os

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

from src.logic.pathes import main_path

_DB_URI = f"sqlite:///{os.path.join(main_path, 'database.db')}"
BASE = declarative_base()

from .equipment import Equipment  # noqa: E402, F401
from .equipmentchecks import EquipmentChecks  # noqa: E402, F401
from .member import Member  # noqa: E402, F401
from .psa import Psa  # noqa: E402, F401
from .specialpsa import SpecialPsa  # noqa: E402, F401
from .specialpsatemplates import SpecialPsaTemplates  # noqa: E402, F401

ENGINE = sqlalchemy.create_engine(_DB_URI)

BASE.metadata.create_all(ENGINE)
DBSession = sqlalchemy.orm.sessionmaker(bind=ENGINE)
session = DBSession()
