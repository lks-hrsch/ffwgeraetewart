import tkinter
from tkinter import ttk

from sqlalchemy import select

import src.models as db
from src.views.viewprotocol import ViewProtocol

treeviewColumns = (
    "type",
    "templatePath",
    "propertyKeys",
    "dateCreated",
    "dateEdited",
)


class SpecialPsaTemplateGUI(ViewProtocol):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.template_tree = ttk.Treeview(self)
        self.init_treeview()
        self.init_treeview_data()
        self.template_tree.pack(fill="both", expand=1)

        self.addframe = tkinter.LabelFrame(self, text="Hinzufügen")
        self.initAddFrame()
        self.addframe.pack(fill="both", expand=1, side=tkinter.LEFT)

        self.alterframe = tkinter.LabelFrame(self, text="Bearbeiten")
        self.initAlterFrame()
        self.alterframe.pack(fill="both", expand=1, side=tkinter.LEFT)

        self.deleteframe = tkinter.LabelFrame(self, text="Löschen")
        self.initDeleteFrame()
        self.deleteframe.pack(fill="both", expand=1, side=tkinter.LEFT)

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
        pass
