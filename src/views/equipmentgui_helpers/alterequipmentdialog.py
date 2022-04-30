import datetime
import tkinter
from tkinter import ttk

import src.models as db

treeviewChecksColumns = (
    "Prüfdatum",
    "Bemerkung",
    "Prüfung Sicht",
    "Prüfung Funktion",
    "Prüfer",
)


class AlterEquipmentDialog:
    def __init__(self, parent, id, name, vendor, year) -> None:
        self.parent = parent
        self.window = tkinter.Toplevel(self.parent)
        self.window.title(name + " - " + str(id))

        self.propertys = [id, name, vendor, year]

        self.checkstree = ttk.Treeview(self.window)

        self.initTreeview()
        self.initData()

        self.detailsframe = tkinter.LabelFrame(self.window, text="Details")
        self.initDetailsFrame()
        self.detailsframe.pack(fill="both", expand=1)

        self.checkstree.pack(fill="both", expand=1)

        self.addframe = tkinter.LabelFrame(self.window, text="Hinzufügen")
        self.initAddFrame()
        self.addframe.pack(fill="both", expand=1, side=tkinter.LEFT)

        # TODO löschen von Checks noch nicht möglich
        # TODO Bearbeiten von checks noch nicht möglich

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
        self.index = 0
        for record in (
            db.session.query(db.EquipmentChecks)
            .filter(db.EquipmentChecks.eid.is_(self.propertys[0]))
            .order_by(db.EquipmentChecks.id)
        ):
            self.checkstree.insert(
                "",
                "end",
                self.index,
                text=record.id,
                values=(
                    record.test_date,
                    record.remark,
                    record.testVision,
                    record.testFunction,
                    record.tester,
                ),
            )
            self.index += 1
        pass

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

        newEquipmentCheck = db.EquipmentChecks(
            id=self.index,
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
            self.index,
            text="",
            values=(test_date, remark, testvision, testfunction, tester),
        )

        self.index += 1
