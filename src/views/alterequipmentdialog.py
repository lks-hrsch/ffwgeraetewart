import datetime
import tkinter
from tkinter import ttk

from sqlalchemy import update

import src.models as db
from src.views.acceptdialog import AcceptDialog
from src.views.uielements import button_pack

treeviewChecksColumns = (
    "Prüfdatum",
    "Bemerkung",
    "Prüfung Sicht",
    "Prüfung Funktion",
    "Prüfer",
)


class AlterEquipmentDialog(tkinter.Toplevel):
    def __init__(self, parent, id, name, vendor, year) -> None:
        super().__init__(parent)
        self.parent = parent
        self.title(f"{name} - {str(id)}")

        self.propertys = [id, name, vendor, year]

        self.checkstree = ttk.Treeview(self)

        self.initTreeview()
        self.initData()

        self.detailsframe = tkinter.LabelFrame(self, text="Details")
        self.initDetailsFrame()
        self.detailsframe.pack(fill="both", expand=1)

        self.checkstree.pack(fill="both", expand=1)

        self.addframe = tkinter.LabelFrame(self, text="Hinzufügen")
        self.initAddFrame()
        self.addframe.pack(fill="both", expand=1, side=tkinter.LEFT)

        self.alterframe = tkinter.LabelFrame(self, text="Bearbeiten")
        self.alterframe.pack(fill="both", expand=1, side=tkinter.LEFT)

        buttons: dict = {
            "Bearbeiten": [self.alterframe, self.commandGetFromTreeview],
            "Speichern": [self.alterframe, self.commandSaveToTreeview],
            "Löschen": [self.alterframe, self.commandDeleteFromTreeview],
        }

        for button_name, button_args in buttons.items():
            button_pack(
                parent_frame=button_args[0],
                label_name=button_name,
                command=button_args[1],
            )

    def initTreeview(self):
        # Columndefinition
        self.checkstree["columns"] = treeviewChecksColumns
        self.checkstree.column("#0", width=25, stretch=tkinter.NO)
        for column in treeviewChecksColumns:
            self.checkstree.column(column, width=130, stretch=tkinter.NO)

        # Columnheader
        self.checkstree.heading("#0", text="ID", anchor=tkinter.W)
        for column in treeviewChecksColumns:
            self.checkstree.heading(column, text=column)

    def initData(self):
        for record in (
            db.session.query(db.EquipmentChecks)
            .filter(db.EquipmentChecks.deleted.is_(False))
            .filter(db.EquipmentChecks.eid.is_(self.propertys[0]))
            .order_by(db.EquipmentChecks.id)
        ):
            self.checkstree.insert(
                "",
                "end",
                record.id,
                text=record.id,
                values=(
                    record.test_date,
                    record.remark,
                    record.testVision,
                    record.testFunction,
                    record.tester,
                ),
            )

    def initDetailsFrame(self):
        tkinter.Label(self.detailsframe, text="Id:").grid(column=0, row=0)
        tkinter.Label(self.detailsframe, text=self.propertys[0]).grid(column=1, row=0)

        tkinter.Label(self.detailsframe, text="Name:").grid(column=0, row=1)
        tkinter.Label(self.detailsframe, text=self.propertys[1]).grid(column=1, row=1)

        tkinter.Label(self.detailsframe, text="Hersteller").grid(column=0, row=2)
        tkinter.Label(self.detailsframe, text=self.propertys[2]).grid(column=1, row=2)

        tkinter.Label(self.detailsframe, text="Jahr").grid(column=0, row=3)
        tkinter.Label(self.detailsframe, text=self.propertys[3]).grid(column=1, row=3)

    def initAddFrame(self):
        iter = 0
        for column in treeviewChecksColumns:
            tkinter.Label(self.addframe, text=column).grid(column=0, row=iter)
            iter += 1

        self.testdateentry = tkinter.Entry(self.addframe)
        self.testdateentry.grid(column=1, row=0)

        self.remarkentry = tkinter.Entry(self.addframe)
        self.remarkentry.grid(column=1, row=1)

        self.testvisioncombobox = ttk.Combobox(self.addframe, values=["i.O.", "n.i.O."])
        self.testvisioncombobox.grid(column=1, row=2)

        self.testfunctioncombobox = ttk.Combobox(self.addframe, values=["i.O.", "n.i.O."])
        self.testfunctioncombobox.grid(column=1, row=3)

        self.testerentry = tkinter.Entry(self.addframe)
        self.testerentry.grid(column=1, row=4)

        addbutton = tkinter.Button(self.addframe, text="Hinzufügen", command=self.commandAddToTreeview)
        addbutton.grid(column=2, row=0, rowspan=(iter + 1))

    def commandAddToTreeview(self):
        test_date = self.testdateentry.get()
        remark = self.remarkentry.get()
        testvision = self.testvisioncombobox.get()
        testfunction = self.testfunctioncombobox.get()
        tester = self.testerentry.get()

        index = 100
        try:
            index = db.session.query(db.EquipmentChecks.id).order_by(db.EquipmentChecks.id.desc()).first()[0] + 1
        except TypeError:
            # may the database is empty
            pass

        newEquipmentCheck = db.EquipmentChecks(
            id=index,
            eid=self.propertys[0],
            test_date=test_date,
            remark=remark,
            testVision=testvision,
            testFunction=testfunction,
            tester=tester,
            dateCreated=datetime.date.today(),
            dateEdited=datetime.date.today(),
            deleted=False,
        )

        db.session.add(newEquipmentCheck)
        db.session.commit()

        self.checkstree.insert(
            "",
            "end",
            index,
            text=index,
            values=(test_date, remark, testvision, testfunction, tester),
        )

    def commandDeleteFromTreeview(self):
        selection = self.checkstree.selection()
        if len(selection) > 0:
            accept_dialog: AcceptDialog = AcceptDialog(self, f"Willst du wirklich: {selection} löschen?")
            if accept_dialog.show():
                for item in selection:
                    tmpitem = self.checkstree.item(item)
                    self.checkstree.delete(item)
                    db.session.execute(
                        update(db.EquipmentChecks)
                        .where(db.EquipmentChecks.id == tmpitem["text"])
                        .values(dateEdited=datetime.date.today(), deleted=True)
                    )
                    db.session.commit()

    def commandGetFromTreeview(self):
        selection = self.checkstree.selection()
        self.testdateentry.delete(0, "end")
        self.remarkentry.delete(0, "end")
        self.testvisioncombobox.delete(0, "end")
        self.testfunctioncombobox.delete(0, "end")
        self.testerentry.delete(0, "end")

        if len(selection) == 1:
            item = self.checkstree.item(selection)
            self.testdateentry.insert(0, item["values"][0])
            self.remarkentry.insert(0, item["values"][1])
            self.testvisioncombobox.insert(0, item["values"][2])
            self.testfunctioncombobox.insert(0, item["values"][3])
            self.testerentry.insert(0, item["values"][4])

    def commandSaveToTreeview(self):
        selection = self.checkstree.selection()
        test_date = self.testdateentry.get()
        remark = self.remarkentry.get()
        testvision = self.testvisioncombobox.get()
        testfunction = self.testfunctioncombobox.get()
        tester = self.testerentry.get()

        if len(selection) == 1:
            self.checkstree.item(selection, values=(test_date, remark, testvision, testfunction, tester))
            item = self.checkstree.item(selection)
            db.session.execute(
                update(db.EquipmentChecks)
                .where(db.EquipmentChecks.id == item["text"])
                .values(
                    test_date=test_date,
                    remark=remark,
                    testVision=testvision,
                    testFunction=testfunction,
                    tester=tester,
                    dateEdited=datetime.date.today(),
                )
            )
            db.session.commit()
