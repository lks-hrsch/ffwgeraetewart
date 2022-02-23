import math
import re

import docx
from docxcompose.composer import Composer

from .paragraph_replace_text import paragraph_replace_text

ALL_DOCUMENTS = {
    "BaseEquipment": "templates/template_equipment.docx",
}


def find_and_replace(document: docx.Document, parameters: dict) -> docx.Document:
    for table in document.tables:
        tmpStyle = table.style
        for rows in table.rows:
            for cell in rows.cells:
                for paragraph in cell.paragraphs:
                    for search, r in parameters.items():
                        paragraph_replace_text(paragraph, re.compile(search), r)
        table.style = tmpStyle
    return document


def compose_single_equipment(parameters: dict):
    doc = docx.Document(ALL_DOCUMENTS["BaseEquipment"])
    find_and_replace(doc, parameters)

    checkRow = ["testdate", "remark", "testVision", "testFunction", "tester"]
    if len(parameters["checks"]) <= 9:
        find_and_replace(doc, {"pagenumber": "1"})
        parameterChecks: dict = {}
        for iterChecks in range(1, 10):
            for check, iter in zip(checkRow, range(0, 5)):
                try:
                    parameterChecks[check + str(iterChecks)] = parameters["checks"][
                        iterChecks - 1
                    ][iter]
                except IndexError:
                    parameterChecks[check + str(iterChecks)] = ""
        find_and_replace(doc, parameterChecks)
        composed_master = Composer(doc)
    else:
        find_and_replace(doc, {"pagenumber": str(1)})
        parameterChecks: dict = {}
        for iterChecks in range(1, 10):
            for check, iter in zip(checkRow, range(0, 5)):
                try:
                    parameterChecks[check + str(iterChecks)] = parameters["checks"][
                        ((1 - 1) * 9) + (iterChecks - 1)
                    ][iter]
                except IndexError:
                    parameterChecks[check + str(iterChecks)] = ""
        find_and_replace(doc, parameterChecks)
        composed_master = Composer(doc)

        for iterPages in range(2, math.ceil(len(parameters["checks"]) / 9) + 1):
            doc = docx.Document(ALL_DOCUMENTS["BaseEquipment"])
            find_and_replace(doc, parameters)
            find_and_replace(doc, {"pagenumber": str(iterPages)})
            parameterChecks: dict = {}
            for iterChecks in range(1, 10):
                for check, iter in zip(checkRow, range(0, 5)):
                    try:
                        parameterChecks[check + str(iterChecks)] = parameters["checks"][
                            ((iterPages - 1) * 9) + (iterChecks - 1)
                        ][iter]
                    except IndexError:
                        parameterChecks[check + str(iterChecks)] = ""
            find_and_replace(doc, parameterChecks)
            composed_master.append(doc)

    composed_master.save("../reports/out.docx")
    return composed_master


def compose_multiple_equipment(parametersList: list):
    first = True
    master = None
    for parameters in parametersList:
        if first:
            master = compose_single_equipment(parameters)
            first = False
        else:
            master.append(compose_single_equipment(parameters).doc)
    master.save("../reports/out.docx")
    pass


def main():
    parameters1 = {
        "devicename": "Lampe",
        "devicenumber": "1234",
        "vendor": "Tesla",
        "create/shipmentdate": "17.05.2015/20.06.2015",
        "checks": [
            ["12.08.2018", "-", "i.O.", "i.O.", "Lukas Hirsch"],
            ["15.07.2019", "-", "i.O.", "i.O.", "Lukas Hirsch"],
            ["05.09.2020", "Kabelbruch", "i.O.", "n.i.O.", "Lukas Hirsch"],
            ["20.10.2021", "-", "i.O.", "i.O.", "Lukas Hirsch"],
            ["31.08.2022", "Verschlamt", "n.i.O.", "i.O.", "Lukas Hirsch"],
        ],
    }

    parameters2 = {
        "devicename": "Lampe",
        "devicenumber": "1234",
        "vendor": "Tesla",
        "create/shipmentdate": "17.05.2015/20.06.2015",
        "checks": [
            ["12.08.2018", "-", "i.O.", "i.O.", "Lukas Hirsch"],
            ["15.07.2019", "-", "i.O.", "i.O.", "Lukas Hirsch"],
            ["05.09.2020", "Kabelbruch", "i.O.", "n.i.O.", "Lukas Hirsch"],
            ["20.10.2021", "-", "i.O.", "i.O.", "Lukas Hirsch"],
            ["31.08.2022", "Verschlamt", "n.i.O.", "i.O.", "Lukas Hirsch"],
            ["12.08.2023", "-", "i.O.", "i.O.", "Lukas Hirsch"],
            ["15.07.2024", "-", "i.O.", "i.O.", "Lukas Hirsch"],
            ["05.09.2025", "Kabelbruch", "i.O.", "n.i.O.", "Lukas Hirsch"],
            ["20.10.2026", "-", "i.O.", "i.O.", "Lukas Hirsch"],
            ["31.08.2027", "Verschlamt", "n.i.O.", "i.O.", "Lukas Hirsch"],
            ["12.08.2028", "-", "i.O.", "i.O.", "Lukas Hirsch"],
            ["15.07.2029", "-", "i.O.", "i.O.", "Lukas Hirsch"],
            ["05.09.2030", "Kabelbruch", "i.O.", "n.i.O.", "Lukas Hirsch"],
            ["20.10.2031", "-", "i.O.", "i.O.", "Lukas Hirsch"],
            ["31.08.2032", "Verschlamt", "n.i.O.", "i.O.", "Lukas Hirsch"],
            ["12.08.2033", "-", "i.O.", "i.O.", "Lukas Hirsch"],
            ["15.07.2034", "-", "i.O.", "i.O.", "Lukas Hirsch"],
            ["05.09.2035", "Kabelbruch", "i.O.", "n.i.O.", "Lukas Hirsch"],
            ["20.10.2036", "-", "i.O.", "i.O.", "Lukas Hirsch"],
            ["31.08.2037", "Verschlamt", "n.i.O.", "i.O.", "Lukas Hirsch"],
            ["12.08.2038", "-", "i.O.", "i.O.", "Lukas Hirsch"],
            ["15.07.2039", "-", "i.O.", "i.O.", "Lukas Hirsch"],
            ["05.09.2040", "Kabelbruch", "i.O.", "n.i.O.", "Lukas Hirsch"],
            ["20.10.2041", "-", "i.O.", "i.O.", "Lukas Hirsch"],
            ["31.08.2042", "Verschlamt", "n.i.O.", "i.O.", "Lukas Hirsch"],
            ["12.08.2043", "-", "i.O.", "i.O.", "Lukas Hirsch"],
            ["15.07.2044", "-", "i.O.", "i.O.", "Lukas Hirsch"],
            ["05.09.2045", "Kabelbruch", "i.O.", "n.i.O.", "Lukas Hirsch"],
            ["20.10.2046", "-", "i.O.", "i.O.", "Lukas Hirsch"],
            ["31.08.2047", "Verschlamt", "n.i.O.", "i.O.", "Lukas Hirsch"],
            ["12.08.2048", "-", "i.O.", "i.O.", "Lukas Hirsch"],
            ["15.07.2049", "-", "i.O.", "i.O.", "Lukas Hirsch"],
            ["05.09.2050", "Kabelbruch", "i.O.", "n.i.O.", "Lukas Hirsch"],
            ["20.10.2051", "-", "i.O.", "i.O.", "Lukas Hirsch"],
            ["31.08.2052", "Verschlamt", "n.i.O.", "i.O.", "Lukas Hirsch"],
        ],
    }

    compose_single_equipment(parameters1)
    compose_single_equipment(parameters2)
    compose_multiple_equipment([parameters1, parameters2])
    pass


if __name__ == "__main__":
    main()
