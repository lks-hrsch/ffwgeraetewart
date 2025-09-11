import datetime
import tkinter

from sqlalchemy import select, update

import src.models as db
from src.views.acceptdialog import AcceptDialog
from src.views.customtreeview import CustomTreeView
from src.views.uielements import button_grid, button_pack, entry_with_label
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

        # for resizing
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self.template_tree = CustomTreeView(self, "ID", treeviewColumns)
        self.init_treeview_data()
        self.template_tree.grid(column=0, row=0, columnspan=2, sticky="nesw")

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
            button_pack(
                parent_frame=button_args[0],
                label_name=button_name,
                command=button_args[1],
            )

    def init_treeview_data(self):
        self.index = 1
        statement = select(db.SpecialPsaTemplates).filter(db.SpecialPsaTemplates.deleted.is_(False))
        for record in db.session.execute(statement).all():
            record = record[0]
            self.template_tree.insert(
                "",
                "end",
                record.id,
                text=record.id,
                values=(
                    record.type,
                    record.templatePath,
                    record.propertyKeys,
                    record.dateCreated,
                    record.dateEdited,
                ),
            )
            self.index += 1

    def initAddFrame(self):
        self.typeentry = entry_with_label(self.addframe, "Typ", 0, 0)
        self.pathentry = entry_with_label(self.addframe, "Pfad", 0, 1)
        self.propertyentry = entry_with_label(self.addframe, "Eigenschaften", 0, 2)

        button_grid(
            parent_frame=self.addframe,
            label_name="Hinzufügen",
            command=self.commandAddToTreeview,
            column=0,
            row=3,
        )

    def commandAddToTreeview(self):
        type = self.typeentry.get()
        path = self.pathentry.get()
        property = self.propertyentry.get()

        index = 100
        try:
            index = (
                db.session.query(db.SpecialPsaTemplates.id).order_by(db.SpecialPsaTemplates.id.desc()).first()[0] + 1
            )
        except TypeError:
            # may the database is empty
            pass

        newSpecialPsaTemplates = db.SpecialPsaTemplates(
            id=index,
            type=type,
            templatePath=path,
            propertyKeys=property,
            dateCreated=datetime.date.today(),
            dateEdited=datetime.date.today(),
            deleted=False,
        )

        db.session.add(newSpecialPsaTemplates)
        db.session.commit()

        self.template_tree.insert(
            "",
            "end",
            index,
            text=index,
            values=(type, path, property),
        )

    def commandDeleteFromTreeview(self):
        selection = self.template_tree.selection()
        if len(selection) > 0:
            accept_dialog: AcceptDialog = AcceptDialog(self, f"Willst du wirklich: {selection} löschen?")
            if accept_dialog.show():
                for item in selection:
                    tmpitem = self.template_tree.item(item)
                    self.template_tree.delete(item)
                    db.session.execute(
                        update(db.SpecialPsaTemplates)
                        .where(db.SpecialPsaTemplates.id == tmpitem["text"])
                        .values(dateEdited=datetime.date.today(), deleted=True)
                    )
                    db.session.commit()

    def commandGetFromTreeview(self):
        self.typeentry.delete(0, "end")
        self.pathentry.delete(0, "end")
        self.propertyentry.delete(0, "end")

        if selected := self.template_tree.ensure_one_selected():
            _, item = selected
            self.typeentry.insert(0, item["values"][0])
            self.pathentry.insert(0, item["values"][1])
            self.propertyentry.insert(0, item["values"][2])

    def commandSaveToTreeview(self):
        type = self.typeentry.get()
        path = self.pathentry.get()
        property = self.propertyentry.get()

        if selected := self.template_tree.ensure_one_selected():
            selection, item = selected
            self.template_tree.item(selection, values=(type, path, property))
            db.session.execute(
                update(db.SpecialPsaTemplates)
                .where(db.SpecialPsaTemplates.id == item["text"])
                .values(
                    type=type,
                    templatePath=path,
                    propertyKeys=property,
                    dateEdited=datetime.date.today(),
                )
            )
            db.session.commit()
