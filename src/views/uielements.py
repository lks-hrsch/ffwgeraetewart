import tkinter

from customtkinter import CTkButton, CTkEntry, CTkFrame, CTkLabel  # type: ignore


def entry_with_label(
    parent_frame: tkinter.LabelFrame | tkinter.Frame | CTkLabel,
    label_name: str,
    column: int,
    row: int,
    column_span: int = 1,
) -> CTkEntry:
    container = CTkFrame(parent_frame)

    label = CTkLabel(container, text=label_name, width=15)
    label.grid(column=0, row=0)
    entry = CTkEntry(container)
    entry.grid(column=1, row=0)

    container.grid(column=column, row=row, columnspan=column_span)
    return entry


def button_pack(
    parent_frame: tkinter.LabelFrame | tkinter.Frame | CTkLabel,
    label_name: str,
    command,
) -> CTkButton:
    button = CTkButton(master=parent_frame, width=200, height=35, text=label_name, command=command)
    button.pack()
    return button


def button_grid(
    parent_frame: tkinter.LabelFrame | tkinter.Frame | CTkLabel,
    label_name: str,
    command,
    column: int,
    row: int,
    columnspan: int = 1,
) -> CTkButton:
    button = CTkButton(master=parent_frame, width=200, height=35, text=label_name, command=command)
    button.grid(column=column, row=row, columnspan=columnspan)
    return button
