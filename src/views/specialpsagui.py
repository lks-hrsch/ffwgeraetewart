"""
Special Psa GUI.

* Schnittschutzhelm
* Schnittschutzhose
* Wathosen
"""
import datetime
import json
import tkinter
from tkinter import ttk

from sqlalchemy import select, update

import src.models as db
import src.template_processing as tp
from src.logic.files import open_file
from src.logic.pathes import out_path
from src.views.acceptdialog import AcceptDialog
from src.views.customtreeview import CustomTreeView
from src.views.uielements import button_pack
from src.views.viewprotocol import ViewProtocol

treeviewColumns = (
    "Typ",
    "Eigenschaften",
    "dateCreated",
    "dateEdited",
)


class SpecialPsaGUI(ViewProtocol):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.parent = parent

        # for resizing
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.rowconfigure(0, weight=1)

        self.special_psa_tree = CustomTreeView(self, "ID", treeviewColumns)
        self.init_treeview_data()
        self.special_psa_tree.grid(column=0, row=0, columnspan=4, sticky="nesw")

        self.addframe = tkinter.LabelFrame(self, text="Hinzufügen")
        self.initAddFrame()
        self.addframe.grid(column=0, row=1, sticky="nesw")

        self.propertyframe = tkinter.LabelFrame(self, text="Eigenschaften")
        self.propertys = None
        self.property_entrys = []

        self.alterframe = tkinter.LabelFrame(self, text="Bearbeiten")
        self.alterframe.grid(column=2, row=1, sticky="nesw")

        buttons: dict = {
            "Bearbeiten": [self.alterframe, self.commandGetFromTreeview],
            "Speichern": [self.alterframe, self.commandSaveToTreeview],
            "Löschen": [self.alterframe, self.commandDeleteFromTreeview],
        }

        for button_name, button_args in buttons.items():
            button_pack(parent_frame=button_args[0], label_name=button_name, command=button_args[1])

        self.printframe = tkinter.LabelFrame(self, text="Drucken")
        self.initPrintFrame()
        self.printframe.grid(column=3, row=1, sticky="nesw")

    def init_treeview_data(self):
        statement = select(db.SpecialPsa).filter(db.SpecialPsa.deleted.is_(False))
        for record in db.session.execute(statement).all():
            self.special_psa_tree.insert(
                "",
                "end",
                record["SpecialPsa"].id,
                text=record["SpecialPsa"].id,
                values=(
                    record["SpecialPsa"].type,
                    record["SpecialPsa"].propertys,
                    record["SpecialPsa"].dateCreated,
                    record["SpecialPsa"].dateEdited,
                ),
            )

    def update_propertys(self, event):
        # destroy all widgets from frame
        for widget in self.propertyframe.winfo_children():
            widget.destroy()

        # this will clear frame and frame will be empty
        # if you want to hide the empty panel then
        self.propertyframe.grid_forget()

        selected_type = self.typecombobox.get()
        self.propertys = db.session.execute(
            select(db.SpecialPsaTemplates.propertyKeys).filter(db.SpecialPsaTemplates.type == selected_type)
        ).one_or_none()
        self.propertys = self.propertys[0].split(" ")

        column = 0
        self.property_entrys = []
        for row, property in enumerate(self.propertys):
            tkinter.Label(self.propertyframe, text=property).grid(column=column, row=row)
            entry = tkinter.Entry(self.propertyframe)
            entry.grid(column=column + 1, row=row)
            self.property_entrys.append(entry)
        self.propertyframe.grid(column=1, row=1, sticky="nesw")

    def fill_propertys(self, propertys):
        propertys_dict: dict = json.loads(propertys)
        for iter, value in enumerate(propertys_dict.values()):
            self.property_entrys[iter].insert(0, value)

    def initAddFrame(self):
        types = db.session.execute(
            select(db.SpecialPsaTemplates.type)
            .filter(db.SpecialPsaTemplates.deleted.is_(False))
            .order_by(db.SpecialPsaTemplates.type)
        ).all()
        types = [x[0] for x in types]

        tkinter.Label(self.addframe, text="Typ").grid(column=0, row=0)
        self.typecombobox = ttk.Combobox(self.addframe, values=types)
        self.typecombobox.bind("<<ComboboxSelected>>", self.update_propertys)
        self.typecombobox.grid(column=1, row=0)

        label = tkinter.Label(self.addframe, text="Name", width=15)
        label.grid(column=0, row=1)
        self.nameentry = tkinter.Entry(self.addframe)
        self.nameentry.grid(column=1, row=1)

        addbutton = tkinter.Button(self.addframe, text="Hinzufügen", command=self.commandAddToTreeview)
        addbutton.grid(column=0, row=2, columnspan=2)

    def initPrintFrame(self):
        printsingleequipmentbutton = tkinter.Button(
            self.printframe,
            text="Selektietes Gerät",
            command=self.commandPrintSingleEquipment,
        )
        printsingleequipmentbutton.pack()

    def commandAddToTreeview(self):
        index: str = self.nameentry.get()
        propertys_dict = dict(zip(self.propertys, [x.get() for x in self.property_entrys]))

        special_psa = db.SpecialPsa(
            id=index,
            type=self.typecombobox.get(),
            propertys=json.dumps(propertys_dict),
            dateCreated=datetime.date.today(),
            dateEdited=datetime.date.today(),
            deleted=False,
        )

        self.special_psa_tree.insert(
            "",
            "end",
            special_psa.id,
            text=special_psa.id,
            values=(
                special_psa.type,
                special_psa.propertys,
                special_psa.dateCreated,
                special_psa.dateEdited,
            ),
        )

        db.session.add(special_psa)
        db.session.commit()

    def commandPrintSingleEquipment(self):
        selection = self.special_psa_tree.selection()
        if len(selection) == 1:
            equipment = self.special_psa_tree.item(selection[0])
            template_path = db.session.execute(
                select(db.SpecialPsaTemplates.templatePath).filter(
                    db.SpecialPsaTemplates.type == equipment["values"][0]
                )
            ).one_or_none()
            template_path = template_path[0]

            parameters = json.loads(equipment["values"][1])
            parameters["number"] = equipment["text"]
            parameters["year"] = datetime.datetime.now().strftime("%Y")

            tp.compose_specificpsa_with_path(parameters, template_path)

            open_file(out_path)

    def commandDeleteFromTreeview(self):
        selection = self.special_psa_tree.selection()
        if len(selection) > 0:
            accept_dialog: AcceptDialog = AcceptDialog(self, f"Willst du wirklich: {selection} löschen?")
            if accept_dialog.show():
                for item in selection:
                    tmpitem = self.special_psa_tree.item(item)
                    self.special_psa_tree.delete(item)
                    db.session.execute(
                        update(db.SpecialPsa)
                        .where(db.SpecialPsa.id == tmpitem["text"])
                        .values(dateEdited=datetime.date.today(), deleted=True)
                    )
                    db.session.commit()

    def commandGetFromTreeview(self):
        selection = self.special_psa_tree.selection()
        self.typecombobox.delete(0, "end")
        self.nameentry.delete(0, "end")

        if len(selection) == 1:
            item = self.special_psa_tree.item(selection)
            self.nameentry.insert(0, item["text"])
            self.typecombobox.insert(0, item["values"][0])

            self.update_propertys(None)
            self.fill_propertys(item["values"][1])

    def commandSaveToTreeview(self):
        selection = self.special_psa_tree.selection()
        type = self.typecombobox.get()
        propertys_dict = dict(zip(self.propertys, [x.get() for x in self.property_entrys]))

        if len(selection) == 1:
            self.special_psa_tree.item(selection, values=(type, propertys_dict))
            db.session.execute(
                update(db.SpecialPsa)
                .where(db.SpecialPsa.id == self.nameentry.get())
                .values(
                    propertys=json.dumps(propertys_dict),
                    dateEdited=datetime.date.today(),
                )
            )
            db.session.commit()
