import tkinter

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
        self.initDataFrame()
        self.dataframe.pack(fill="both", expand="yes")

        self.buttonframe = tkinter.LabelFrame(self.window, text="Buttons")
        self.initButtonFrame()
        self.buttonframe.pack(fill="both", expand="yes")

    def initDataFrame(self):
        self.entrys = []
        iter = 0
        for field in treeviewColumns:
            tkinter.Label(self.dataframe, text=field).grid(column=0, row=iter)
            entry = tkinter.Entry(self.dataframe)
            entry.insert(0, self.propertys[iter])
            entry.grid(column=1, row=iter)
            self.entrys.append(entry)
            iter += 1

    def initButtonFrame(self):
        tkinter.Button(
            self.buttonframe, text="Abbruch", command=self.commandAbord
        ).pack(fill="both", expand="yes", side=tkinter.LEFT)
        tkinter.Button(
            self.buttonframe, text="Speichern", command=self.commandSave
        ).pack(fill="both", expand="yes", side=tkinter.LEFT)

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
