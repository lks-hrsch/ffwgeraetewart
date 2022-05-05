import datetime
import os

import src.models as db
from src.logic.convert import join_array
from src.logic.pathes import main_path


def add_special_psa() -> None:
    templates = [
        db.SpecialPsaTemplates(
            type="Wathosen",
            templatePath=os.path.join(main_path, "templates/template_wathose.docx"),
            propertyKeys=join_array(["year", "number", "lastname", "firstname"]),
            dateCreated=datetime.date.today(),
            dateEdited=datetime.date.today(),
            deleted=False,
        ),
        db.SpecialPsaTemplates(
            type="Schnittschutzhose",
            templatePath=os.path.join(main_path, "templates/template_schnittschutzhose.docx"),
            propertyKeys=join_array(["year", "number", "cyear", "lastname", "firstname"]),
            dateCreated=datetime.date.today(),
            dateEdited=datetime.date.today(),
            deleted=False,
        ),
    ]

    for template in templates:
        db.session.add(template)

    db.session.commit()
