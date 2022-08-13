import datetime

import src.models as db
from src.logic.convert import join_array


def add_special_psa() -> None:
    templates = [
        db.SpecialPsaTemplates(
            type="Wathosen",
            templatePath="templates/template_wathose.docx",
            propertyKeys=join_array([]),
            dateCreated=datetime.date.today(),
            dateEdited=datetime.date.today(),
            deleted=False,
        ),
        db.SpecialPsaTemplates(
            type="Schnittschutzhose",
            templatePath="templates/template_schnittschutzhose.docx",
            propertyKeys=join_array(["cyear"]),
            dateCreated=datetime.date.today(),
            dateEdited=datetime.date.today(),
            deleted=False,
        ),
    ]

    for template in templates:
        db.session.add(template)

    db.session.commit()
