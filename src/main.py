import tkinter
from typing import Type

from src.views.equipmentgui import EquipmentGUI
from src.views.membergui import MemberGUI
from src.views.psagui import PsaGUI
from src.views.specialpsagui import SpecialPsaGUI
from src.views.viewprotocol import ViewProtocol


class MainGUI(tkinter.Tk):
    frames: dict[str, Type[MemberGUI] | Type[PsaGUI] | Type[SpecialPsaGUI] | Type[EquipmentGUI]] = {
        "MemberGUI": MemberGUI,
        "PsaGUI": PsaGUI,
        "SpecialPsaGUI": SpecialPsaGUI,
        "EquipmentGUI": EquipmentGUI,
    }

    def __init__(self, *args, **kwargs) -> None:  # type: ignore
        tkinter.Tk.__init__(self, *args, **kwargs)

        self.title("ffwgerätewart")
        # self.geometry("200x200")

        menubar = tkinter.Menu(self)
        self.config(menu=menubar)

        member_menu = tkinter.Menu(menubar)
        member_menu.add_command(label="Anzeigen", command=lambda: self.show_frame("MemberGUI"))

        psa_menu = tkinter.Menu(menubar)
        psa_menu.add_command(label="Normale PSA", command=lambda: self.show_frame("PsaGUI"))
        psa_menu.add_command(label="Spezielle PSA", command=lambda: self.show_frame("SpecialPsaGUI"))

        equipment_menu = tkinter.Menu(menubar)
        equipment_menu.add_command(label="Anzeigen", command=lambda: self.show_frame("EquipmentGUI"))

        menubar.add_cascade(label="Mitglieder", menu=member_menu, underline=0)
        menubar.add_cascade(label="PSA", menu=psa_menu, underline=0)
        menubar.add_cascade(label="Equipment", menu=equipment_menu, underline=0)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        self.container = tkinter.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)

        self.show_frame("MemberGUI")

    def show_frame(self, page_name: str) -> None:
        """Show a frame for the given page name"""
        try:
            self.frame.destroy()
        except AttributeError as ex:
            pass

        view_class: Type[MemberGUI] | Type[PsaGUI] | Type[SpecialPsaGUI] | Type[EquipmentGUI] | None = self.frames.get(
            page_name
        )
        self.frame: ViewProtocol = view_class(parent=self.container)  # type: ignore
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.frame.tkraise()


def main() -> None:
    app: tkinter.Tk = MainGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
