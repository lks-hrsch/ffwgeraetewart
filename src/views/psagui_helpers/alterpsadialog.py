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


class AlterPsaDialog:
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
        self.parent = parent
        self.window = tkinter.Toplevel(self.parent)
        self.window.title(name)

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
        self.ret = self.propertys

        self.dataframe = tkinter.LabelFrame(self.window, text="Daten")
        self.entrys = self.initDataFrame()
        self.dataframe.pack(fill="both", expand=1)

        self.buttonframe = tkinter.LabelFrame(self.window, text="Buttons")
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
        self.ret = self.propertys
        self.window.destroy()

    def commandSave(self):
        self.ret = []
        for entry in self.entrys:
            self.ret.append(entry.get())
        self.window.destroy()

    def show(self):
        self.window.deiconify()
        self.window.wait_window()
        return self.ret
