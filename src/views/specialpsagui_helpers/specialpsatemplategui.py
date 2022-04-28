import datetime
import tkinter
from tkinter import ttk

from sqlalchemy import select

import src.models as db

treeviewColumns = (
    "type",
    "templatePath",
    "propertyKeys",
    "dateCreated",
    "dateEdited",
)


def join_array(array: list[str]) -> str:
    """
    Join text.

    :param array:
    :return:
    """
    return " ".join(array)


class SpecialPsaTemplateDialog:
    def __init__(self, parent):
        self.parent = parent
        self.window = tkinter.Toplevel(self.parent)
        self.window.title("Templateverwaltung für PSA Kleidung")
        self.ret = None

        self.template_tree = ttk.Treeview(self.window)
        self.init_treeview()
        self.init_treeview_data()
        self.template_tree.pack(fill="both", expand=1)

        self.addframe = tkinter.LabelFrame(self.window, text="Hinzufügen")
        self.initAddFrame()
        self.addframe.pack(fill="both", expand=1, side=tkinter.LEFT)

        self.alterframe = tkinter.LabelFrame(self.window, text="Bearbeiten")
        self.initAlterFrame()
        self.alterframe.pack(fill="both", expand=1, side=tkinter.LEFT)

        self.deleteframe = tkinter.LabelFrame(self.window, text="Löschen")
        self.initDeleteFrame()
        self.deleteframe.pack(fill="both", expand=1, side=tkinter.LEFT)

    def show(self):
        self.window.deiconify()
        self.window.wait_window()
        return self.ret

    def init_treeview(self):
        # Columndefinition
        self.template_tree["columns"] = treeviewColumns
        self.template_tree.column("#0", width=100, stretch=tkinter.NO)
        for column in treeviewColumns:
            self.template_tree.column(column, width=130, stretch=tkinter.NO)

        # Columnheader
        self.template_tree.heading("#0", text="Name", anchor=tkinter.W)
        for column in treeviewColumns:
            self.template_tree.heading(column, text=column)

    def init_treeview_data(self):
        self.index = 1
        statement = select(db.SpecialPsaTemplates).filter(db.SpecialPsaTemplates.deleted.is_(False))
        for record in db.session.execute(statement).all():
            self.template_tree.insert(
                "",
                "end",
                record["SpecialPsaTemplates"].id,
                text=record["SpecialPsaTemplates"].id,
                values=(
                    record["SpecialPsaTemplates"].type,
                    record["SpecialPsaTemplates"].templatePath,
                    record["SpecialPsaTemplates"].propertyKeys,
                    record["SpecialPsaTemplates"].dateCreated,
                    record["SpecialPsaTemplates"].dateEdited,
                ),
            )
            self.index += 1

    def initAddFrame(self):
        add_button = tkinter.Button(self.addframe, text="Hinzufügen", command=self.commandAddToTreeview)
        add_button.pack()
        pass

    def initAlterFrame(self):
        pass

    def initDeleteFrame(self):
        pass

    def commandAddToTreeview(self):
        templates = [
            db.SpecialPsaTemplates(
                type="Wathosen",
                templatePath="templates/template_wathose.docx",
                propertyKeys=join_array(["year", "number", "lastname", "firstname"]),
                dateCreated=datetime.date.today(),
                dateEdited=datetime.date.today(),
                deleted=False,
            ),
            db.SpecialPsaTemplates(
                type="Schnittschutzhose",
                templatePath="templates/template_schnittschutzhose.docx",
                propertyKeys=join_array(["year", "number", "cyear", "lastname", "firstname"]),
                dateCreated=datetime.date.today(),
                dateEdited=datetime.date.today(),
                deleted=False,
            ),
        ]

        for template in templates:
            self.template_tree.insert(
                "",
                "end",
                self.index,
                text=self.index,
                values=(
                    template.type,
                    template.templatePath,
                    template.propertyKeys,
                    template.dateCreated,
                    template.dateEdited,
                ),
            )
            db.session.add(template)
            self.index += 1

        db.session.commit()
        pass
