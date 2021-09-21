"""
Special Psa GUI.

* Schnittschutzhelm
* Schnittschutzhose
* Wathosen
"""

import tkinter


"""
 TODO Create new Template
            * Templatepath
 TODO Alter Template
 TODO Delete Template
 TODO Create new Special Psa
 TODO Alter Special Psa
 TODO Delete Special Psa
 TODO Print Special Psa
"""


class SpecialPsaGUI:
    def __init__(self, parent) -> None:
        self.parent = parent
        self.window = tkinter.Toplevel(self.parent)
        self.window.title("Special - PSA")

    pass
