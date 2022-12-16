import datetime
import tkinter

from sqlalchemy import update

import src.models as db
from src.views.acceptdialog import AcceptDialog
from src.views.customtreeview import CustomTreeView
from src.views.uielements import button_grid, button_pack, entry_with_label
from src.views.viewprotocol import ViewProtocol

treeviewColumns = ("Nachname", "Vorname")


class MemberGUI(ViewProtocol):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.parent = parent

        # for resizing
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self.membertree = CustomTreeView(self, "ID", treeviewColumns)
        self.initData()
        self.membertree.grid(column=0, row=0, columnspan=2, sticky="nesw")

        self.addframe = tkinter.LabelFrame(self, text="Hinzufügen")
        self.initAddFrame()
        self.addframe.grid(column=0, row=1, sticky="nesw")

        self.alterframe = tkinter.LabelFrame(self, text="Bearbeiten")
        self.alterframe.grid(column=1, row=1, sticky="nesw")

        buttons: dict = {
            "Bearbeiten": [self.alterframe, self.commandGetFromTreeview],
            "Speichern": [self.alterframe, self.commandSaveToTreeview],
            "Löschen": [self.alterframe, self.commandDeleteFromTreeview],
        }

        for button_name, button_args in buttons.items():
            button_pack(parent_frame=button_args[0], label_name=button_name, command=button_args[1])

    def initData(self):
        for member in db.Member.get_all(db.session):
            self.membertree.insert(
                "",
                "end",
                member.id,
                text=member.id,
                values=(member.lastname, member.firstname),
            )

    def initAddFrame(self):
        self.id_entry = entry_with_label(self.addframe, "ID", 0, 0)
        self.firstnameentry = entry_with_label(self.addframe, "Vorname", 0, 1)
        self.lastnameentry = entry_with_label(self.addframe, "Nachname", 0, 2)

        button_grid(
            parent_frame=self.addframe, label_name="Hinzufügen", command=self.commandAddToTreeview, column=0, row=3
        )

    def commandAddToTreeview(self):
        member_id = self.id_entry.get()

        if len(member_id) != 4:
            _: AcceptDialog = AcceptDialog(self, "ID muss 4 Zeichen lang sein")
            return

        firstname = self.firstnameentry.get()
        lastname = self.lastnameentry.get()

        newPsa = db.Psa(
            mid=member_id,
            dateCreated=datetime.date.today(),
            dateEdited=datetime.date.today(),
            deleted=False,
        )
        newMember = db.Member(
            id=member_id,
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
            member_id,
            text=member_id,
            values=(lastname, firstname),
        )

    def commandDeleteFromTreeview(self):
        selection = self.membertree.selection()
        if len(selection) > 0:
            accept_dialog: AcceptDialog = AcceptDialog(self, f"Willst du wirklich: {selection} löschen?")
            if accept_dialog.show():
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
        self.firstnameentry.delete(0, "end")
        self.lastnameentry.delete(0, "end")

        if selected := self.membertree.ensure_one_selected():
            _, item = selected
            self.firstnameentry.insert(0, item["values"][1])
            self.lastnameentry.insert(0, item["values"][0])

    def commandSaveToTreeview(self):
        firstname = self.firstnameentry.get()
        lastname = self.lastnameentry.get()

        if selected := self.membertree.ensure_one_selected():
            selection, item = selected
            self.membertree.item(selection, values=(lastname, firstname))
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
