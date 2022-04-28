import tkinter

from src.views.equipmentgui import EquipmentGUI
from src.views.membergui import MemberGUI
from src.views.psagui import PsaGUI
from src.views.specialpsagui import SpecialPsaGUI


class MainGUI:
    def __init__(self, parent) -> None:
        self.parent = parent
        self.frame = tkinter.Frame(self.parent)
        self.frame.pack()

        buttonMemberGui = tkinter.Button(
            self.frame,
            text="Mitglieder",
            command=self.showMemberGUI,
            padx=5,
            pady=5,
        )
        buttonMemberGui.pack()

        buttonPsaGui = tkinter.Button(self.frame, text="PSA", command=self.showPsaGUI, padx=5, pady=5)
        buttonPsaGui.pack()

        buttonSpecialPsaGui = tkinter.Button(
            self.frame,
            text="Special PSA",
            command=self.showSpecialPsaGUI,
            padx=5,
            pady=5,
        )
        buttonSpecialPsaGui.pack()

        buttonEquipmentGui = tkinter.Button(
            self.frame,
            text="Geräte",
            command=self.showEquipmentGUI,
            padx=5,
            pady=5,
        )
        buttonEquipmentGui.pack()
        pass

    def showMemberGUI(self):
        MemberGUI(self.parent)

    def showPsaGUI(self):
        PsaGUI(self.parent)

    def showSpecialPsaGUI(self):
        SpecialPsaGUI(self.parent)

    def showEquipmentGUI(self):
        EquipmentGUI(self.parent)


if __name__ == "__main__":
    root = tkinter.Tk()
    root.title("ffwgerätewart")
    root.geometry("200x200")
    launchpad = MainGUI(root)
    root.mainloop()
