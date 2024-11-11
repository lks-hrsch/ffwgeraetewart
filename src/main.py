import tkinter
from typing import Type

from src.logic.initialize_database import add_special_psa
from src.logic.logger import logger
from src.views.equipmentgui import EquipmentGUI
from src.views.membergui import MemberGUI
from src.views.psagui import PsaGUI
from src.views.specialpsagui import SpecialPsaGUI
from src.views.specialpsatemplategui import SpecialPsaTemplateGUI
from src.views.viewprotocol import ViewProtocol


class App(tkinter.Tk):
    frames: dict[
        str,
        Type[MemberGUI] | Type[PsaGUI] | Type[SpecialPsaGUI] | Type[SpecialPsaTemplateGUI] | Type[EquipmentGUI],
    ] = {
        "MemberGUI": MemberGUI,
        "PsaGUI": PsaGUI,
        "SpecialPsaGUI": SpecialPsaGUI,
        "SpecialPsaTemplateGUI": SpecialPsaTemplateGUI,
        # "EquipmentGUI": EquipmentGUI,
    }

    def __init__(self, *args, **kwargs) -> None:  # type: ignore
        tkinter.Tk.__init__(self, *args, **kwargs)

        self.title("ffw-geraetewart")
        # self.geometry("200x200")

        menubar = tkinter.Menu(self)
        self.config(menu=menubar)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        member_menu = tkinter.Menu(menubar)
        member_menu.add_command(label="Anzeigen", command=lambda: self.show_frame("MemberGUI"))

        psa_menu = tkinter.Menu(menubar)
        psa_menu.add_command(label="Normale PSA", command=lambda: self.show_frame("PsaGUI"))
        psa_menu.add_command(label="Spezielle PSA", command=lambda: self.show_frame("SpecialPsaGUI"))
        psa_menu.add_command(
            label="Spezielle PSA Vorlagen",
            command=lambda: self.show_frame("SpecialPsaTemplateGUI"),
        )

        # equipment_menu = tkinter.Menu(menubar)
        # equipment_menu.add_command(label="Anzeigen", command=lambda: self.show_frame("EquipmentGUI"))

        about_menu = tkinter.Menu(menubar)
        about_menu.add_command(
            label="Initialisieren Spezieller PSA Vorlagen",
            command=lambda: add_special_psa(),
        )

        menubar.add_cascade(label="Mitglieder", menu=member_menu, underline=0)
        menubar.add_cascade(label="PSA", menu=psa_menu, underline=0)
        # menubar.add_cascade(label="Equipment", menu=equipment_menu, underline=0)
        menubar.add_cascade(label="Über", menu=about_menu, underline=0)

        self.show_frame("MemberGUI")

    def show_frame(self, page_name: str) -> None:
        """Show a frame for the given page name"""
        try:
            self.frame.destroy()
        except AttributeError:
            pass

        view_class: (
            Type[MemberGUI]
            | Type[PsaGUI]
            | Type[SpecialPsaGUI]
            | Type[SpecialPsaTemplateGUI]
            | Type[EquipmentGUI]
            | None
        ) = self.frames.get(page_name)
        self.frame: ViewProtocol = view_class(parent=self)  # type: ignore
        self.frame.grid(row=0, column=0, sticky="nesw")
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.tkraise()


def handle_exception(exception, value, traceback):
    logger.exception(exception)


def main() -> None:
    logger.info("start app")
    app: tkinter.Tk = App()
    app.report_callback_exception = handle_exception
    app.mainloop()
    logger.info("stop app")


if __name__ == "__main__":
    main()
