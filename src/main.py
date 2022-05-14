import tkinter
from typing import Type

import customtkinter  # type: ignore

from src.logic.initialize_database import add_special_psa
from src.views.equipmentgui import EquipmentGUI
from src.views.membergui import MemberGUI
from src.views.psagui import PsaGUI
from src.views.specialpsagui import SpecialPsaGUI
from src.views.specialpsatemplategui import SpecialPsaTemplateGUI
from src.views.viewprotocol import ViewProtocol


class App(customtkinter.CTk):  # type: ignore
    frames: dict[
        str, Type[MemberGUI] | Type[PsaGUI] | Type[SpecialPsaGUI] | Type[SpecialPsaTemplateGUI] | Type[EquipmentGUI]
    ] = {
        "MemberGUI": MemberGUI,
        "PsaGUI": PsaGUI,
        "SpecialPsaGUI": SpecialPsaGUI,
        "SpecialPsaTemplateGUI": SpecialPsaTemplateGUI,
        "EquipmentGUI": EquipmentGUI,
    }

    def __init__(self) -> None:
        super().__init__()

        self.title("ffw-geraetewart")
        # self.geometry("200x200")

        menubar = tkinter.Menu(self)
        self.config(menu=menubar)

        member_menu = tkinter.Menu(menubar)
        member_menu.add_command(label="Anzeigen", command=lambda: self.show_frame("MemberGUI"))

        psa_menu = tkinter.Menu(menubar)
        psa_menu.add_command(label="Normale PSA", command=lambda: self.show_frame("PsaGUI"))
        psa_menu.add_command(label="Spezielle PSA", command=lambda: self.show_frame("SpecialPsaGUI"))
        psa_menu.add_command(label="Spezielle PSA Vorlagen", command=lambda: self.show_frame("SpecialPsaTemplateGUI"))

        equipment_menu = tkinter.Menu(menubar)
        equipment_menu.add_command(label="Anzeigen", command=lambda: self.show_frame("EquipmentGUI"))

        about_menu = tkinter.Menu(menubar)
        about_menu.add_command(label="Initialisieren Spezieller PSA Vorlagen", command=lambda: add_special_psa())

        menubar.add_cascade(label="Mitglieder", menu=member_menu, underline=0)
        menubar.add_cascade(label="PSA", menu=psa_menu, underline=0)
        menubar.add_cascade(label="Equipment", menu=equipment_menu, underline=0)
        menubar.add_cascade(label="Über", menu=about_menu, underline=0)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        self.container = customtkinter.CTkFrame(self)
        self.container.pack(side="top", fill="both", expand=True)

        self.show_frame("MemberGUI")

    def show_frame(self, page_name: str) -> None:
        """Show a frame for the given page name"""
        try:
            self.frame.destroy()
        except AttributeError as ex:
            pass

        view_class: Type[MemberGUI] | Type[PsaGUI] | Type[SpecialPsaGUI] | Type[SpecialPsaTemplateGUI] | Type[
            EquipmentGUI
        ] | None = self.frames.get(page_name)
        self.frame: ViewProtocol = view_class(parent=self.container)  # type: ignore
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.frame.tkraise()


def main() -> None:
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")

    app: customtkinter.CTk = App()
    app.mainloop()


if __name__ == "__main__":
    main()
