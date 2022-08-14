import datetime
import tkinter
from tkinter import ttk

from sqlalchemy import update

import src.models as db
import src.template_processing as tp
from src.logic.equipmenttypes import EquipmentTypes
from src.logic.files import open_file
from src.logic.logger import logger
from src.logic.pathes import out_path
from src.views.acceptdialog import AcceptDialog
from src.views.alterequipmentdialog import AlterEquipmentDialog
from src.views.customtreeview import CustomTreeView
from src.views.uielements import button_grid, button_pack, entry_with_label
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

        # for resizing
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)

        self.equipmenttree = CustomTreeView(self, "ID", treeviewColumns)
        self.initData()
        self.equipmenttree.grid(column=0, row=0, columnspan=3, sticky="nesw")

        self.addframe = tkinter.LabelFrame(self, text="Hinzufügen")
        self.initAddFrame()
        self.addframe.grid(column=0, row=1, sticky="nesw")

        self.alterframe = tkinter.LabelFrame(self, text="Bearbeiten")
        self.alterframe.grid(column=1, row=1, sticky="nesw")

        self.printframe = tkinter.LabelFrame(self, text="Drucken")
        self.printframe.grid(column=2, row=1, sticky="nesw")

        buttons: dict = {
            "Anzeigen": [self.alterframe, self.commandShowSelected],
            "Löschen": [self.alterframe, self.commandDeleteFromTreeview],
            "Selektietes Gerät": [self.printframe, self.commandPrintSingleEquipment],
            "Selektietes Gerät Blanko": [self.printframe, self.commandPrintSingleEquipmentBlanko],
            "Alle Geräte": [self.printframe, self.commandPrintAllEquipments],
            "Alle Geräte Blanko": [self.printframe, self.commandPrintAllEquipmentsBlanko],
        }

        for button_name, button_args in buttons.items():
            button_pack(parent_frame=button_args[0], label_name=button_name, command=button_args[1])

    def initData(self):
        # init Parents
        for rubrik in EquipmentTypes:
            self.equipmenttree.insert("", "end", rubrik.value, text=rubrik.name)

        # init Data
        for equipment in db.Equipment.get_all(db.session):
            self.equipmenttree.insert(
                equipment.category,
                "end",
                equipment.id,
                text=equipment.id,
                values=(equipment.name, equipment.vendor, equipment.year, "", ""),
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

        button_grid(
            parent_frame=self.addframe,
            label_name="Hinzufügen",
            command=self.commandAddToTreeview,
            column=0,
            row=5,
            columnspan=2,
        )

    def commandAddToTreeview(self):
        equipmenttype = self.equipmentcombobox.get()
        id = self.identry.get()
        name = self.nameentry.get()
        vendor = self.vendorentry.get()
        year = self.yearentry.get()

        if (equipmenttype == "") or (id == "") or (name == ""):
            logger.info("missing Value")
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

    def commandDeleteFromTreeview(self):
        selection = self.equipmenttree.selection()
        if len(selection) > 0:
            accept_dialog: AcceptDialog = AcceptDialog(self, f"Willst du wirklich: {selection} löschen?")
            if accept_dialog.show():
                for item in selection:
                    tmpitem = self.equipmenttree.item(item)
                    self.equipmenttree.delete(item)
                    db.session.execute(
                        update(db.Equipment)
                        .where(db.Equipment.id == tmpitem["text"])
                        .values(dateEdited=datetime.date.today(), deleted=True)
                    )
                    db.session.commit()

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

    def commandPrintSingleEquipment(self):
        selection = self.equipmenttree.selection()
        if len(selection) == 1:
            item = self.equipmenttree.item(selection)
            equipment: db.Equipment = db.Equipment.get_by_id(item["text"], db.session)

            if len(equipment.checks) == 0:
                return self.commandPrintSingleEquipmentBlanko()

            parameterEquipment: dict = {
                "devicename": equipment.name,
                "devicenumber": equipment.id,
                "vendor": equipment.vendor,
                "create/shipmentdate": equipment.year,
                "checks": [
                    [
                        check.test_date,
                        check.remark,
                        check.testVision,
                        check.testFunction,
                        check.tester,
                    ]
                    for check in equipment.checks
                ],
            }

            tp.compose_multiple_equipment([parameterEquipment])
            open_file(out_path)

    def commandPrintSingleEquipmentBlanko(self):
        selection = self.equipmenttree.selection()
        if len(selection) == 1:
            item = self.equipmenttree.item(selection)
            equipment: db.Equipment = db.Equipment.get_by_id(item["text"], db.session)

            parameterEquipment: dict = {
                "devicename": equipment.name,
                "devicenumber": equipment.id,
                "vendor": equipment.vendor,
                "create/shipmentdate": equipment.year,
                "checks": [],
            }

            tp.compose_multiple_equipment([parameterEquipment])
            open_file(out_path)

    def commandPrintAllEquipments(self):
        equipments: list[db.Equipment] = db.Equipment.get_all(db.session)

        parameterEquipmentList = [
            {
                "devicename": equipment.name,
                "devicenumber": equipment.id,
                "vendor": equipment.vendor,
                "create/shipmentdate": equipment.year,
                "checks": [
                    [
                        check.test_date,
                        check.remark,
                        check.testVision,
                        check.testFunction,
                        check.tester,
                    ]
                    for check in equipment.checks
                ],
            }
            for equipment in equipments
        ]

        tp.compose_multiple_equipment(parameterEquipmentList)
        open_file(out_path)

    def commandPrintAllEquipmentsBlanko(self):
        equipments: list[db.Equipment] = db.Equipment.get_all(db.session)

        parameterEquipmentList = [
            {
                "devicename": equipment.name,
                "devicenumber": equipment.id,
                "vendor": equipment.vendor,
                "create/shipmentdate": equipment.year,
                "checks": [],
            }
            for equipment in equipments
        ]

        tp.compose_multiple_equipment(parameterEquipmentList)
        open_file(out_path)
