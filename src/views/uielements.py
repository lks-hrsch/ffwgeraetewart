import tkinter


def entry_with_label(
    parent_frame: tkinter.LabelFrame | tkinter.Frame,
    label_name: str,
    column: int,
    row: int,
    column_span: int = 1,
) -> tkinter.Entry:
    container = tkinter.Frame(parent_frame)

    label = tkinter.Label(container, text=label_name, width=15)
    label.grid(column=0, row=0)
    entry = tkinter.Entry(container)
    entry.grid(column=1, row=0)

    container.grid(column=column, row=row, columnspan=column_span)
    return entry


def button_pack(
    parent_frame: tkinter.LabelFrame | tkinter.Frame,
    label_name: str,
    command,
) -> tkinter.Button:
    button = tkinter.Button(master=parent_frame, width=15, text=label_name, command=command)
    button.pack()
    return button


def button_grid(
    parent_frame: tkinter.LabelFrame | tkinter.Frame,
    label_name: str,
    command,
    column: int,
    row: int,
    columnspan: int = 1,
) -> tkinter.Button:
    button = tkinter.Button(master=parent_frame, width=15, text=label_name, command=command)
    button.grid(column=column, row=row, columnspan=columnspan)
    return button
