"""
Special Psa GUI.

* Schnittschutzhelm
* Schnittschutzhose
* Wathosen
"""
import datetime
import json
import os
import platform
import subprocess
import tkinter
from tkinter import ttk
from sqlalchemy import select

import src.models as db

from .specialpsagui_helpers.specialpsatemplategui import SpecialPsaTemplateDialog
import src.template_processing as tp

"""
 TODO Create new Template
 TODO Alter Template
 TODO Delete Template
 TODO Create new Special Psa
 TODO Alter Special Psa
 TODO Delete Special Psa
 TODO Print Special Psa
"""

treeviewColumns = (
    "Typ",
    "Gerätename",
    "Eigenschaften",
    "dateCreated",
    "dateEdited"
)


class SpecialPsaGUI:
    def __init__(self, parent) -> None:
        self.parent = parent
        self.window = tkinter.Toplevel(self.parent)
        self.window.title("Special - PSA")

        self.special_psa_tree = ttk.Treeview(self.window)
        self.init_treeview()
        self.init_treeview_data()
        self.special_psa_tree.pack(fill="both", expand="yes", side=tkinter.TOP)

        self.addframe = tkinter.LabelFrame(self.window, text="Hinzufügen")
        self.initAddFrame()
        self.addframe.pack(fill="both", expand="yes", side=tkinter.LEFT)

        self.propertyframe = tkinter.LabelFrame(self.window, text="Eigenschaften")
        self.propertys = None
        self.property_entrys = []

        self.templateframe = tkinter.LabelFrame(self.window, text="Vorlagen")
        self.init_template_frame()
        self.templateframe.pack(fill="both", expand="yes", side=tkinter.RIGHT)

        self.printframe = tkinter.LabelFrame(self.window, text="Drucken")
        self.initPrintFrame()
        self.printframe.pack(fill="both", expand="yes", side=tkinter.LEFT)

        self.deleteframe = tkinter.LabelFrame(self.window, text="Löschen")
        self.initDeleteFrame()
        self.deleteframe.pack(fill="both", expand="yes", side=tkinter.RIGHT)

        self.alterframe = tkinter.LabelFrame(self.window, text="Bearbeiten")
        self.initAlterFrame()
        self.alterframe.pack(fill="both", expand="yes", side=tkinter.RIGHT)

    def init_treeview(self):
        # Columndefinition
        self.special_psa_tree["columns"] = treeviewColumns
        self.special_psa_tree.column("#0", width=100, stretch=tkinter.NO)
        for column in treeviewColumns:
            self.special_psa_tree.column(column, width=130, stretch=tkinter.NO)

        # Columnheader
        self.special_psa_tree.heading("#0", text="Name", anchor=tkinter.W)
        for column in treeviewColumns:
            self.special_psa_tree.heading(column, text=column)

    def init_treeview_data(self):
        self.index = 1
        statement = (
            select(db.SpecialPsa)
            .filter(db.SpecialPsa.deleted.is_(False))
        )
        for record in db.session.execute(statement).all():
            self.special_psa_tree.insert(
                "",
                "end",
                record["SpecialPsa"].id,
                text=record["SpecialPsa"].id,
                values=(
                    record["SpecialPsa"].type,
                    record["SpecialPsa"].number,
                    record["SpecialPsa"].propertys,
                    record["SpecialPsa"].dateCreated,
                    record["SpecialPsa"].dateEdited
                ),
            )
            self.index += 1

    def update_propertys(self, event):
        # destroy all widgets from frame
        for widget in self.propertyframe.winfo_children():
            widget.destroy()

        # this will clear frame and frame will be empty
        # if you want to hide the empty panel then
        self.propertyframe.pack_forget()

        selected_type = self.typecombobox.get()
        self.propertys = db.session.execute(
            select(db.SpecialPsaTemplates.propertyKeys).filter(db.SpecialPsaTemplates.type == selected_type)
        ).one_or_none()
        self.propertys = self.propertys[0].split(" ")

        column = 0
        row = 0
        self.property_entrys = []
        for property in self.propertys:
            tkinter.Label(self.propertyframe, text=property).grid(column=column, row=row)
            entry = tkinter.Entry(self.propertyframe)
            entry.grid(column=column + 1, row=row)
            self.property_entrys.append(entry)
            row += 1

        self.propertyframe.pack(fill="both", expand="yes", side=tkinter.LEFT)
        pass

    def initAddFrame(self):
        types = db.session.execute(
            select(db.SpecialPsaTemplates.type).order_by(db.SpecialPsaTemplates.type)
        ).all()
        types = [x[0] for x in types]

        tkinter.Label(self.addframe, text="Typ").grid(column=0, row=0)
        self.typecombobox = ttk.Combobox(
            self.addframe,
            values=types
        )
        self.typecombobox.bind('<<ComboboxSelected>>', self.update_propertys)
        self.typecombobox.grid(column=1, row=0)

        tkinter.Label(self.addframe, text="Name").grid(column=0, row=1)
        self.nameentry = tkinter.Entry(self.addframe)
        self.nameentry.grid(column=1, row=1)

        addbutton = tkinter.Button(
            self.addframe, text="Hinzufügen", command=self.commandAddToTreeview
        )
        addbutton.grid(column=0, row=2, columnspan=2)
        pass

    def initAlterFrame(self):
        pass

    def initDeleteFrame(self):
        pass

    def initPrintFrame(self):
        printsingleequipmentbutton = tkinter.Button(
            self.printframe,
            text="Selektietes Gerät",
            command=self.commandPrintSingleEquipment,
        )
        printsingleequipmentbutton.pack()

    def init_template_frame(self):
        alterbutton = tkinter.Button(
            self.templateframe, text="Bearbeiten", command=self.commandOpenTemplateView
        )
        alterbutton.pack()
        pass

    def commandAddToTreeview(self):
        propertys_dict = dict(zip(self.propertys, [x.get() for x in self.property_entrys]))

        special_psa = db.SpecialPsa(
            type=self.typecombobox.get(),
            number=self.nameentry.get(),
            propertys=json.dumps(propertys_dict),
            dateCreated=datetime.date.today(),
            dateEdited=datetime.date.today(),
            deleted=False,
        )

        self.special_psa_tree.insert(
            "",
            "end",
            self.index,
            text=self.index,
            values=(
                special_psa.type,
                special_psa.number,
                special_psa.propertys,
                special_psa.dateCreated,
                special_psa.dateEdited
            ),
        )
        self.index += 1

        db.session.add(special_psa)
        db.session.commit()
        pass

    def commandPrintSingleEquipment(self):
        selection = self.special_psa_tree.selection()
        if len(selection) == 1:
            equipment = self.special_psa_tree.item(selection[0])
            template_path = db.session.execute(
                select(db.SpecialPsaTemplates.templatePath).filter(db.SpecialPsaTemplates.type == equipment["values"][0])
            ).one_or_none()
            template_path = template_path[0]

            parameters = json.loads(equipment["values"][2])
            tp.compose_specificpsa_with_path(parameters, template_path)

            if platform.system() == "Darwin":  # macOS
                subprocess.call(("open", "../reports/out.docx"))
            elif platform.system() == "Windows":  # Windows
                os.startfile("../reports/out.docx")
        pass

    def commandOpenTemplateView(self):
        ret = SpecialPsaTemplateDialog(self.window).show()
        pass

