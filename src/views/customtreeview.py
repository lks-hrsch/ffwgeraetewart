import tkinter
from tkinter import ttk


class CustomTreeView(ttk.Treeview):
    def __init__(self, parent, id_column_name: str, other_column_names: tuple) -> None:
        super().__init__(parent)

        # Columndefinition
        self["columns"] = other_column_names
        self.column("#0", minwidth=50, width=150, stretch=tkinter.NO)

        # Columnheader
        self.heading("#0", text=id_column_name, anchor=tkinter.W)

        for column in other_column_names:
            self.column(column, stretch=tkinter.YES)
            self.heading(column, text=column)

    def ensure_one_selected(self):
        selection = self.selection()
        return (selection, self.item(selection)) if len(selection) == 1 else None
