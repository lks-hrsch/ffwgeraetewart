import tkinter


class AcceptDialog(tkinter.Toplevel):
    """

    popup = AcceptDialog(root, f"Do you really want to delete: {x}")
    if popup.show():
        # go ahead
    """

    def __init__(self, parent, text: str) -> None:
        super().__init__(parent)
        self.parent = parent
        self.title("Bestätigen")
        self.returning: bool = False

        accept_label = tkinter.Label(self, text=text)
        accept_label.pack()

        accept_button = tkinter.Button(self, text="Bestätigen", command=self.command_accept)
        accept_button.pack()

        abort_button = tkinter.Button(self, text="Abbrechen", command=self.command_abort)
        abort_button.pack()

    def show(self) -> bool:
        self.deiconify()
        self.wm_protocol("WM_DELETE_WINDOW", self.destroy)
        self.wait_window(self)
        return self.returning

    def command_accept(self) -> None:
        self.returning = True
        self.destroy()

    def command_abort(self) -> None:
        self.returning = False
        self.destroy()
