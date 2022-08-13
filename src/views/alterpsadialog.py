import tkinter

from src.views.uielements import entry_with_label

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


class AlterPsaDialog(tkinter.Toplevel):
    def __init__(
        self,
        parent,
        name,
        eJacke,
        eHose,
        aJacke,
        aHose,
        hNummer,
        hDatum,
        sHandschuhe,
        sSchuhwerk,
        kHaube,
    ) -> None:
        super().__init__(parent)
        self.parent = parent
        self.title(name)

        self.propertys = [
            eJacke,
            eHose,
            aJacke,
            aHose,
            hNummer,
            hDatum,
            sHandschuhe,
            sSchuhwerk,
            kHaube,
        ]
        self.returning = self.propertys

        self.dataframe = tkinter.LabelFrame(self, text="Daten")
        self.entrys = self.initDataFrame()
        self.dataframe.pack(fill="both", expand=1)

        self.buttonframe = tkinter.LabelFrame(self, text="Buttons")
        self.initButtonFrame()
        self.buttonframe.pack(fill="both", expand=1)

    def initDataFrame(self) -> list[tkinter.Entry]:
        entrys: list[tkinter.Entry] = []
        for index, field in enumerate(treeviewColumns):
            entry = entry_with_label(self.dataframe, field, 0, index, 2)
            entry.insert(0, self.propertys[index])  # type: ignore
            entrys.append(entry)
        return entrys

    def initButtonFrame(self):
        tkinter.Button(self.buttonframe, text="Abbruch", command=self.commandAbord).pack(
            fill="both", expand=1, side=tkinter.LEFT
        )
        tkinter.Button(self.buttonframe, text="Speichern", command=self.commandSave).pack(
            fill="both", expand=1, side=tkinter.LEFT
        )

    def commandAbord(self):
        self.returning = self.propertys
        self.destroy()

    def commandSave(self):
        self.returning = [entry.get() for entry in self.entrys]
        self.destroy()

    def show(self):
        self.deiconify()
        self.wait_window()
        return self.returning
