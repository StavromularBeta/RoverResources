import tkinter as tk
from GUI.GUI_formatting import GUI_formatting as tk_formatting


class LoginView(tk.Frame):

    def __init__(self, parent, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)
        self.parent = parent
        self.formatting = tk_formatting.TkFormattingMethods()

    def login_view(self):
        tk.Label(self, text="Login View").grid()
