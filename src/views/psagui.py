import datetime
import os
import platform
import subprocess
import tkinter
from tkinter import ttk

from sqlalchemy import select, update

import src.models as db
import src.template_processing as tp
from src.pathes import out_path
from src.views.psagui_helpers.alterpsadialog import AlterPsaDialog

treeviewColumns = (
    "EinsatzkleidungJacke",
    "EinsatzkleidungHose",
    "ArbeitskleidungJacke",
    "ArbeitskleidungHose",
    "HelmNummer",
    "HelmDatum",
    "Schutzhandschuhe",
    "Sicherheitsschuwerk",
    "Kopfschutzhaube",
)


class PsaGUI:
    def __init__(self, parent) -> None:
        self.parent = parent
        self.window = tkinter.Toplevel(self.parent)
        self.window.title("PSA")
        self.psatree = ttk.Treeview(self.window)

        self.init_treeview()
        self.init_data()

        self.psatree.pack()

        self.alterframe = tkinter.LabelFrame(self.window, text="Bearbeiten")
        self.init_alter_frame()
        self.alterframe.pack(fill="both", expand=1, side=tkinter.LEFT)

        self.printframe = tkinter.LabelFrame(self.window, text="Drucken")
        self.initPrintFrame()
        self.printframe.pack(fill="both", expand=1, side=tkinter.LEFT)

    def init_treeview(self):
        # Columndefinition
        self.psatree["columns"] = treeviewColumns
        self.psatree.column("#0", width=100, stretch=tkinter.NO)
        for column in treeviewColumns:
            self.psatree.column(column, width=130, stretch=tkinter.NO)

        # Columnheader
        self.psatree.heading("#0", text="Name", anchor=tkinter.W)
        for column in treeviewColumns:
            self.psatree.heading(column, text=column)

    def init_data(self):
        self.index = 1
        statement = (
            select(db.Psa, db.Member).join(db.Member).filter(db.Member.deleted.is_(False)).order_by(db.Member.lastname)
        )
        for record in db.session.execute(statement).all():
            self.psatree.insert(
                "",
                "end",
                record["Psa"].id,
                text=record["Member"].lastname + " " + record["Member"].firstname,
                values=(
                    record["Psa"].eJacke,
                    record["Psa"].eHose,
                    record["Psa"].aJacke,
                    record["Psa"].aHose,
                    record["Psa"].hNummer,
                    record["Psa"].hDate,
                    record["Psa"].sGloves,
                    record["Psa"].sShoe,
                    record["Psa"].kHaube,
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
        selection = self.psatree.selection()
        if len(selection) == 1:
            item = self.psatree.item(selection)
            ret = AlterPsaDialog(
                self.window,
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
            ).show()
            self.psatree.item(selection, values=ret)
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
                    sShoe=ret[7],
                    kHaube=ret[8],
                    dateEdited=datetime.date.today(),
                )
            )
            db.session.commit()
        pass

    def commandPrintSingleMember(self):
        parameters: dict

        selection = self.psatree.selection()
        if len(selection) == 1:
            statement = (
                select(db.Psa, db.Member)
                .join(db.Member)
                .filter(db.Psa.id.is_(selection[0]))
                .filter(db.Member.deleted.is_(False))
                .order_by(db.Member.lastname)
            )
            for record in db.session.execute(statement).all():
                parameters = {
                    "year": "2020",
                    "lastname": record["Member"].lastname,
                    "firstname": record["Member"].firstname,
                    "numaj": record["Psa"].aJacke,
                    "numah": record["Psa"].aHose,
                    "numej": record["Psa"].eJacke,
                    "numeh": record["Psa"].eHose,
                    "numhand": record["Psa"].sGloves,
                    "numhelm": record["Psa"].hNummer,
                    "yhelm": record["Psa"].hDate,
                    "numkopf": record["Psa"].kHaube,
                    "numschuhe": record["Psa"].sShoe,
                }

            tp.compose_specificpsa_for_member(parameters, self.psatypecombobox.get())

            if platform.system() == "Darwin":  # macOS
                subprocess.call(("open", out_path))
            elif platform.system() == "Windows":  # Windows
                os.startfile(out_path)
        pass

    def commandPrintWholeMember(self):
        parameters = []

        selection = self.psatree.selection()
        if len(selection) == 1:
            statement = (
                select(db.Psa, db.Member)
                .join(db.Member)
                .filter(db.Psa.id.is_(selection[0]))
                .filter(db.Member.deleted.is_(False))
                .order_by(db.Member.lastname)
            )
            for record in db.session.execute(statement).all():
                param = {
                    "year": "2020",
                    "lastname": record["Member"].lastname,
                    "firstname": record["Member"].firstname,
                    "numaj": record["Psa"].aJacke,
                    "numah": record["Psa"].aHose,
                    "numej": record["Psa"].eJacke,
                    "numeh": record["Psa"].eHose,
                    "numhand": record["Psa"].sGloves,
                    "numhelm": record["Psa"].hNummer,
                    "yhelm": record["Psa"].hDate,
                    "numkopf": record["Psa"].kHaube,
                    "numschuhe": record["Psa"].sShoe,
                }
                parameters.append(param)

            tp.compose_wholepsa(parameters)

            if platform.system() == "Darwin":  # macOS
                subprocess.call(("open", out_path))
            elif platform.system() == "Windows":  # Windows
                os.startfile(out_path)
        pass

    def commandPrintAll(self):
        parameters = []

        statement = (
            select(db.Psa, db.Member).join(db.Member).filter(db.Member.deleted.is_(False)).order_by(db.Member.lastname)
        )
        for record in db.session.execute(statement).all():
            param = {
                "year": "2020",
                "lastname": record["Member"].lastname,
                "firstname": record["Member"].firstname,
                "numaj": record["Psa"].aJacke,
                "numah": record["Psa"].aHose,
                "numej": record["Psa"].eJacke,
                "numeh": record["Psa"].eHose,
                "numhand": record["Psa"].sGloves,
                "numhelm": record["Psa"].hNummer,
                "yhelm": record["Psa"].hDate,
                "numkopf": record["Psa"].kHaube,
                "numschuhe": record["Psa"].sShoe,
            }
            parameters.append(param)

        tp.compose_wholepsa(parameters)

        if platform.system() == "Darwin":  # macOS
            subprocess.call(("open", out_path))
        elif platform.system() == "Windows":  # Windows
            os.startfile(out_path)
        pass
