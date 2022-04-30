import datetime
import tkinter
from tkinter import ttk

from sqlalchemy import update

import src.models as db
from src.views.uielements import entry_with_label
from src.views.viewprotocol import ViewProtocol


class MemberGUI(ViewProtocol):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.parent = parent
        self.membertree = ttk.Treeview(self)

        self.initTreeview()
        self.initData()

        self.membertree.pack(fill="both", expand=1, side=tkinter.TOP)

        self.addframe = tkinter.LabelFrame(self, text="Hinzufügen")
        self.initAddFrame()
        self.addframe.pack(fill="both", expand=1, side=tkinter.LEFT)

        self.alterframe = tkinter.LabelFrame(self, text="Bearbeiten")
        self.initAlterFrame()
        self.alterframe.pack(fill="both", expand=1, side=tkinter.LEFT)

    def initTreeview(self):
        # Columndefinition
        self.membertree["columns"] = ("Nachname", "Vorname")
        self.membertree.column("#0", width=270, stretch=tkinter.NO)
        self.membertree.column("Nachname", width=150, stretch=tkinter.NO)
        self.membertree.column("Vorname", width=400)

        # Columnheader
        self.membertree.heading("#0", text="ID", anchor=tkinter.W)
        self.membertree.heading("Nachname", text="Nachname", anchor=tkinter.W)
        self.membertree.heading("Vorname", text="Vorname", anchor=tkinter.W)

    def initData(self):
        for record in db.session.query(db.Member).filter(db.Member.deleted.is_(False)).order_by(db.Member.lastname):
            self.membertree.insert(
                "",
                "end",
                record.id,
                text=record.id,
                values=(record.lastname, record.firstname),
            )

    def initAddFrame(self):
        self.firstnameentry = entry_with_label(self.addframe, "Vorname", 0, 0)
        self.lastnameentry = entry_with_label(self.addframe, "Nachname", 0, 1)

        addbutton = tkinter.Button(self.addframe, text="Hinzufügen", command=self.commandAddToTreeview)
        addbutton.grid(column=0, row=2)

    def initAlterFrame(self):
        alterbutton = tkinter.Button(
            self.alterframe,
            text="Bearbeiten",
            command=self.commandGetFromTreeview,
        )
        alterbutton.pack()

        savebutton = tkinter.Button(
            self.alterframe,
            text="Speichern",
            command=self.commandSaveToTreeview,
        )
        savebutton.pack()

        deletebutton = tkinter.Button(
            self.alterframe,
            text="Löschen",
            command=self.commandDeleteFromTreeview,
        )
        deletebutton.pack()

    def commandAddToTreeview(self):
        firstname = self.firstnameentry.get()
        lastname = self.lastnameentry.get()
        index = db.session.query(db.Member.id).order_by(db.Member.id.desc()).first()[0] + 1

        newPsa = db.Psa(
            mid=index,
            dateCreated=datetime.date.today(),
            dateEdited=datetime.date.today(),
            deleted=False,
        )
        newMember = db.Member(
            id=index,
            firstname=firstname,
            lastname=lastname,
            dateCreated=datetime.date.today(),
            dateEdited=datetime.date.today(),
            deleted=False,
            psa=newPsa,
        )

        db.session.add(newPsa)
        db.session.add(newMember)
        db.session.commit()

        self.membertree.insert(
            "",
            "end",
            index,
            text=index,
            values=(lastname, firstname),
        )

    def commandDeleteFromTreeview(self):
        selection = self.membertree.selection()
        if len(selection) > 0:
            for item in selection:
                tmpitem = self.membertree.item(item)
                self.membertree.delete(item)
                db.session.execute(
                    update(db.Member)
                    .where(db.Member.id == tmpitem["text"])
                    .values(dateEdited=datetime.date.today(), deleted=True)
                )
                db.session.commit()

    def commandGetFromTreeview(self):
        selection = self.membertree.selection()
        self.firstnameentry.delete(0, "end")
        self.lastnameentry.delete(0, "end")
        if len(selection) == 1:
            item = self.membertree.item(selection)
            self.firstnameentry.insert(0, item["values"][1])
            self.lastnameentry.insert(0, item["values"][0])

    def commandSaveToTreeview(self):
        selection = self.membertree.selection()
        firstname = self.firstnameentry.get()
        lastname = self.lastnameentry.get()

        if len(selection) == 1:
            self.membertree.item(selection, values=(lastname, firstname))
            item = self.membertree.item(selection)
            db.session.execute(
                update(db.Member)
                .where(db.Member.id == item["text"])
                .values(
                    lastname=lastname,
                    firstname=firstname,
                    dateEdited=datetime.date.today(),
                )
            )
            db.session.commit()
