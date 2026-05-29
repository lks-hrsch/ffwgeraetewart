import datetime
import tkinter
from tkinter import ttk

from sqlalchemy import select, update

import src.models as db
import src.template_processing as tp
from src.logic.files import open_file
from src.logic.pathes import out_path
from src.views.alterpsadialog import AlterPsaDialog
from src.views.customtreeview import CustomTreeView
from src.views.viewprotocol import ViewProtocol

treeviewColumns = (
    "EinsatzkleidungJacke",
    "EinsatzkleidungHose",
    "ArbeitskleidungJacke",
    "ArbeitskleidungHose",
    "HelmNummer",
    "HelmDatum",
    "Schutzhandschuhe",
    "TH-Handschuhe",
    "Sicherheitsschuwerk",
    "Kopfschutzhaube",
)


class PsaGUI(ViewProtocol):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.parent = parent

        # for resizing
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self.psatree = CustomTreeView(self, "Name", treeviewColumns)
        self.init_data()
        self.psatree.grid(column=0, row=0, columnspan=2, sticky="nesw")

        self.alterframe = tkinter.LabelFrame(self, text="Bearbeiten")
        self.init_alter_frame()
        self.alterframe.grid(column=0, row=1, sticky="nesw")

        self.printframe = tkinter.LabelFrame(self, text="Drucken")
        self.initPrintFrame()
        self.printframe.grid(column=1, row=1, sticky="nesw")

    def init_data(self):
        self.index = 1
        statement = (
            select(db.Psa, db.Member).join(db.Member).filter(db.Member.deleted.is_(False)).order_by(db.Member.lastname)
        )
        for record in db.session.execute(statement).all():
            self.psatree.insert(
                "",
                "end",
                record[0].id,
                text=f"{record[1].lastname} {record[1].firstname}",
                values=(
                    record[0].eJacke,
                    record[0].eHose,
                    record[0].aJacke,
                    record[0].aHose,
                    record[0].hNummer,
                    record[0].hDate,
                    record[0].sGloves,
                    record[0].sTAGloves,
                    record[0].sShoe,
                    record[0].kHaube,
                ),
            )
            self.index += 1

    def init_alter_frame(self):
        alterbutton = tkinter.Button(
            self.alterframe,
            text="Bearbeiten",
            command=self.commandOpenAlterView,
        )
        alterbutton.pack()

    def initPrintFrame(self):
        self.psatypecombobox = ttk.Combobox(
            self.printframe,
            values=[
                "Arbeitskleidung",
                "Einsatzkleidung",
                "Handschuhe",
                "TH-Handschuhe",
                "Helm",
                "Kopfschutzhaube",
                "Schuhe",
            ],
        )
        self.psatypecombobox.grid(column=0, row=0)

        printsinglepsabutton = tkinter.Button(
            self.printframe,
            text="Selektietes Mitglied + Selektierte PSA",
            command=self.commandPrintSingleMember,
        )
        printsinglepsabutton.grid(column=1, row=0)

        printsinglememberbutton = tkinter.Button(
            self.printframe,
            text="Selektietes Mitglied",
            command=self.commandPrintWholeMember,
        )
        printsinglememberbutton.grid(column=0, row=1, columnspan=2)

        printallmemberbutton = tkinter.Button(
            self.printframe,
            text="Alle Mitglieder",
            command=self.commandPrintAll,
        )
        printallmemberbutton.grid(column=0, row=2, columnspan=2)

    def commandOpenAlterView(self):
        if selected := self.psatree.ensure_one_selected():
            selection, item = selected
            ret = AlterPsaDialog(
                self,
                item["text"],
                item["values"][0],
                item["values"][1],
                item["values"][2],
                item["values"][3],
                item["values"][4],
                item["values"][5],
                item["values"][6],
                item["values"][7],
                item["values"][8],
                item["values"][9],
            ).show()
            self.psatree.item(
                selection, values=(ret[0], ret[1], ret[2], ret[3], ret[4], ret[5], ret[6], ret[7], ret[8], ret[9])
            )
            db.session.execute(
                update(db.Psa)
                .where(db.Psa.id == selection[0])
                .values(
                    eJacke=ret[0],
                    eHose=ret[1],
                    aJacke=ret[2],
                    aHose=ret[3],
                    hNummer=ret[4],
                    hDate=ret[5],
                    sGloves=ret[6],
                    sTAGloves=ret[7],
                    sShoe=ret[8],
                    kHaube=ret[9],
                    dateEdited=datetime.date.today(),
                )
            )
            db.session.commit()

    @staticmethod
    def _get_parameter_from_query(query: list) -> list:
        parameters = []

        for record in query:
            param = {
                "year": datetime.datetime.now().strftime("%Y"),
                "lastname": record[1].lastname,
                "firstname": record[1].firstname,
                "numaj": record[0].aJacke,
                "numah": record[0].aHose,
                "numej": record[0].eJacke,
                "numeh": record[0].eHose,
                "numhand": record[0].sGloves,
                "numthhand": record[0].sTAGloves,
                "numhelm": record[0].hNummer,
                "yhelm": record[0].hDate,
                "numkopf": record[0].kHaube,
                "numschuhe": record[0].sShoe,
            }

            parameters.append(param)

        return parameters

    def commandPrintSingleMember(self):
        if selected := self.psatree.ensure_one_selected():
            selection, _ = selected
            statement = (
                select(db.Psa, db.Member)
                .join(db.Member)
                .filter(db.Psa.id.is_(selection[0]))
                .filter(db.Member.deleted.is_(False))
                .order_by(db.Member.lastname)
            )

            parameters: dict = self._get_parameter_from_query(db.session.execute(statement).all())[0]  # type: ignore

            tp.compose_specificpsa_for_member(parameters, self.psatypecombobox.get())

            open_file(out_path)

    def commandPrintWholeMember(self):
        if selected := self.psatree.ensure_one_selected():
            selection, _ = selected
            statement = (
                select(db.Psa, db.Member)
                .join(db.Member)
                .filter(db.Psa.id.is_(selection[0]))
                .filter(db.Member.deleted.is_(False))
                .order_by(db.Member.lastname)
            )

            parameters: list = self._get_parameter_from_query(db.session.execute(statement).all())

            tp.compose_wholepsa(parameters)

            open_file(out_path)

    def commandPrintAll(self):
        statement = (
            select(db.Psa, db.Member).join(db.Member).filter(db.Member.deleted.is_(False)).order_by(db.Member.lastname)
        )

        parameters: list = self._get_parameter_from_query(db.session.execute(statement).all())

        tp.compose_wholepsa(parameters)

        open_file(out_path)
