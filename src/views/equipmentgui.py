import datetime
import os
import platform
import subprocess
import tkinter
from tkinter import ttk

from sqlalchemy import select, update

import src.models as db
import src.template_processing as tp
from src.logic.pathes import out_path
from src.views.equipmentgui_helpers.alterequipmentdialog import AlterEquipmentDialog
from src.views.equipmentgui_helpers.equipmenttypes import EquipmentTypes
from src.views.uielements import entry_with_label
from src.views.viewprotocol import ViewProtocol

treeviewColumns = (
    "Gerätename",
    "Hersteller",
    "Herstellungs-/Lieferjahr",
    "Letzte Prüfung",
    "Letzte Bemerkung",
)


class EquipmentGUI(ViewProtocol):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.parent = parent
        self.equipmenttree = ttk.Treeview(self)

        self.initTreeview()
        self.initData()

        self.equipmenttree.pack(fill="both", expand=1)

        self.addframe = tkinter.LabelFrame(self, text="Hinzufügen")
        self.initAddFrame()
        self.addframe.pack(fill="both", expand=1, side=tkinter.LEFT)

        self.alterframe = tkinter.LabelFrame(self, text="Bearbeiten")
        self.initAlterFrame()
        self.alterframe.pack(fill="both", expand=1, side=tkinter.LEFT)

        self.printframe = tkinter.LabelFrame(self, text="Drucken")
        self.initPrintFrame()
        self.printframe.pack(fill="both", expand=1, side=tkinter.LEFT)

    def initTreeview(self):
        # Columndefinition
        self.equipmenttree["columns"] = treeviewColumns
        self.equipmenttree.column("#0", width=200, stretch=tkinter.NO)
        for column in treeviewColumns:
            self.equipmenttree.column(column, width=130, stretch=tkinter.NO)

        # Columnheader
        self.equipmenttree.heading("#0", text="ID", anchor=tkinter.W)
        for column in treeviewColumns:
            self.equipmenttree.heading(column, text=column)

    def initData(self):
        # init Parents
        for rubrik in EquipmentTypes:
            self.equipmenttree.insert("", "end", rubrik.value, text=rubrik.name)

        # init Data
        for record in db.session.query(db.Equipment).filter(db.Equipment.deleted.is_(False)).order_by(db.Equipment.id):
            self.equipmenttree.insert(
                record.category,
                "end",
                record.id,
                text=record.id,
                values=(record.name, record.vendor, record.year, "", ""),
            )

    def initAddFrame(self):
        tkinter.Label(self.addframe, text="Rubrik").grid(column=0, row=0)
        self.equipmentcombobox = ttk.Combobox(
            self.addframe,
            values=[
                EquipmentTypes.ELEKTRISCHESGERÄT.name,
                EquipmentTypes.TECHNISCHESGERÄT.name,
                EquipmentTypes.WASSERFÜHRENDEARMATUREN.name,
            ],
        )
        self.equipmentcombobox.grid(column=1, row=0)

        self.identry = entry_with_label(self.addframe, "ID", 0, 1, 2)
        self.nameentry = entry_with_label(self.addframe, "Name", 0, 2, 2)
        self.vendorentry = entry_with_label(self.addframe, "Hersteller", 0, 3, 2)
        self.yearentry = entry_with_label(self.addframe, "Jahr", 0, 4, 2)

        addbutton = tkinter.Button(self.addframe, text="Hinzufügen", command=self.commandAddToTreeview)
        addbutton.grid(column=0, row=5, columnspan=2)

    def initAlterFrame(self):
        alterbutton = tkinter.Button(self.alterframe, text="Anzeigen", command=self.commandShowSelected)
        alterbutton.pack()

        deletebutton = tkinter.Button(
            self.alterframe,
            text="Löschen",
            command=self.commandDeleteFromTreeview,
        )
        deletebutton.pack()

    def initPrintFrame(self):
        printsingleequipmentbutton = tkinter.Button(
            self.printframe,
            text="Selektietes Gerät",
            command=self.commandPrintSingleEquipment,
        )
        printsingleequipmentbutton.pack()

        printsingleequipmentblankobutton = tkinter.Button(
            self.printframe,
            text="Selektietes Gerät Blanko",
            command=self.commandPrintSingleEquipmentBlanko,
        )
        printsingleequipmentblankobutton.pack()

        printallequipmentbutton = tkinter.Button(
            self.printframe,
            text="Alle Geräte",
            command=self.commandPrintAllEquipments,
        )
        printallequipmentbutton.pack()

        printallequipmentblankobutton = tkinter.Button(
            self.printframe,
            text="Alle Geräte Blanko",
            command=self.commandPrintAllEquipmentsBlanko,
        )
        printallequipmentblankobutton.pack()
        pass

    def commandAddToTreeview(self):
        equipmenttype = self.equipmentcombobox.get()
        id = self.identry.get()
        name = self.nameentry.get()
        vendor = self.vendorentry.get()
        year = self.yearentry.get()

        if (equipmenttype == "") or (id == "") or (name == ""):
            print("missing Value")
            return

        for rubrik in EquipmentTypes:
            if equipmenttype == rubrik.name:
                equipmenttype = rubrik.value
                break

        self.equipmenttree.insert(
            equipmenttype,
            "end",
            id,
            text=id,
            values=(name, vendor, year, "", ""),
        )

        newEquipment = db.Equipment(
            id=id,
            name=name,
            category=equipmenttype,
            vendor=vendor,
            year=year,
            dateCreated=datetime.date.today(),
            dateEdited=datetime.date.today(),
            deleted=False,
        )

        db.session.add(newEquipment)
        db.session.commit()

        self.identry.delete(0, "end")
        self.nameentry.delete(0, "end")
        pass

    def commandDeleteFromTreeview(self):
        selection = self.equipmenttree.selection()
        if len(selection) > 0:
            for item in selection:
                tmpitem = self.equipmenttree.item(item)
                self.equipmenttree.delete(item)
                db.session.execute(
                    update(db.Equipment)
                    .where(db.Equipment.id == tmpitem["text"])
                    .values(dateEdited=datetime.date.today(), deleted=True)
                )
                db.session.commit()
        pass

    def commandShowSelected(self):
        selection = self.equipmenttree.selection()
        if len(selection) == 1:
            item = self.equipmenttree.item(selection)
            AlterEquipmentDialog(
                self,
                item["text"],
                item["values"][0],
                item["values"][1],
                item["values"][2],
            )
        pass

    def commandPrintSingleEquipment(self):
        parameterEquipment = {}

        selection = self.equipmenttree.selection()
        if len(selection) == 1:
            item = self.equipmenttree.item(selection)
            statement = (
                select(db.Equipment, db.EquipmentChecks)
                .join(db.EquipmentChecks)
                .filter(db.Equipment.id.is_(item["text"]))
                .filter(db.Equipment.deleted.is_(False))
            )

            data = db.session.execute(statement).all()
            if len(data) == 0:
                return self.commandPrintSingleEquipmentBlanko()

            first = True
            for equipment, equipmentcheck in data:
                if first:
                    parameterEquipment["devicename"] = equipment.name
                    parameterEquipment["devicenumber"] = equipment.id
                    parameterEquipment["vendor"] = equipment.vendor
                    parameterEquipment["create/shipmentdate"] = equipment.year
                    parameterEquipment["checks"] = []
                    first = False
                check = [
                    equipmentcheck.test_date,
                    equipmentcheck.remark,
                    equipmentcheck.testVision,
                    equipmentcheck.testFunction,
                    equipmentcheck.tester,
                ]
                parameterEquipment["checks"].append(check)

            tp.compose_multiple_equipment([parameterEquipment])

            if platform.system() == "Darwin":  # macOS
                subprocess.call(("open", out_path))
            elif platform.system() == "Windows":  # Windows
                os.startfile(out_path)
        pass

    def commandPrintSingleEquipmentBlanko(self):
        parameterEquipment = {}

        selection = self.equipmenttree.selection()
        if len(selection) == 1:
            item = self.equipmenttree.item(selection)
            statement = (
                select(db.Equipment).filter(db.Equipment.id.is_(item["text"])).filter(db.Equipment.deleted.is_(False))
            )
            for record in db.session.execute(statement).all():
                parameterEquipment["devicename"] = record[0].name
                parameterEquipment["devicenumber"] = record[0].id
                parameterEquipment["vendor"] = record[0].vendor
                parameterEquipment["create/shipmentdate"] = record[0].year
                parameterEquipment["checks"] = []

            tp.compose_multiple_equipment([parameterEquipment])

            if platform.system() == "Darwin":  # macOS
                subprocess.call(("open", out_path))
            elif platform.system() == "Windows":  # Windows
                os.startfile(out_path)
        pass

    def commandPrintAllEquipments(self):
        parameterEquipmentList = []

        statement = select(db.Equipment).filter(db.Equipment.deleted.is_(False))
        for record in db.session.execute(statement).all():
            parameterEquipment = {}
            parameterEquipment["devicename"] = record[0].name
            parameterEquipment["devicenumber"] = record[0].id
            parameterEquipment["vendor"] = record[0].vendor
            parameterEquipment["create/shipmentdate"] = record[0].year
            parameterEquipment["checks"] = []

            statement = (
                select(db.EquipmentChecks)
                .filter(db.EquipmentChecks.eid.is_(record[0].id))
                .filter(db.EquipmentChecks.deleted.is_(False))
            )
            for record in db.session.execute(statement).all():
                check = [
                    record[0].test_date,
                    record[0].remark,
                    record[0].testVision,
                    record[0].testFunction,
                    record[0].tester,
                ]
                parameterEquipment["checks"].append(check)

            parameterEquipmentList.append(parameterEquipment)

        tp.compose_multiple_equipment(parameterEquipmentList)

        if platform.system() == "Darwin":  # macOS
            subprocess.call(("open", out_path))
        elif platform.system() == "Windows":  # Windows
            os.startfile(out_path)
        pass

    def commandPrintAllEquipmentsBlanko(self):
        parameterEquipmentList = []

        statement = select(db.Equipment).filter(db.Equipment.deleted.is_(False))
        for record in db.session.execute(statement).all():
            parameterEquipment = {}
            parameterEquipment["devicename"] = record[0].name
            parameterEquipment["devicenumber"] = record[0].id
            parameterEquipment["vendor"] = record[0].vendor
            parameterEquipment["create/shipmentdate"] = record[0].year
            parameterEquipment["checks"] = []

            parameterEquipmentList.append(parameterEquipment)

        tp.compose_multiple_equipment(parameterEquipmentList)

        if platform.system() == "Darwin":  # macOS
            subprocess.call(("open", out_path))
        elif platform.system() == "Windows":  # Windows
            os.startfile(out_path)
        pass
